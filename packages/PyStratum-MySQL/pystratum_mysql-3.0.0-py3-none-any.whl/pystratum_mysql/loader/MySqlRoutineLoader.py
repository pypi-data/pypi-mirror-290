import re

from mysql import connector
from pystratum_backend.StratumIO import StratumIO
from pystratum_common.exception.LoaderException import LoaderException
from pystratum_common.loader.CommonRoutineLoader import CommonRoutineLoader
from pystratum_common.loader.helper.CommonDataTypeHelper import CommonDataTypeHelper
from pystratum_common.loader.helper.LoaderContext import LoaderContext

from pystratum_mysql.loader.helper.MySqlDataTypeHelper import MySqlDataTypeHelper
from pystratum_mysql.MySqlMetadataDataLayer import MySqlMetadataDataLayer


class MySqlRoutineLoader(CommonRoutineLoader):
    """
    Class for loading a single stored routine into a MySQL instance from a (pseudo) SQL file.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 io: StratumIO,
                 dl: MySqlMetadataDataLayer,
                 sql_mode: str,
                 character_set: str,
                 collate: str):
        """
        Object constructor.

        :param io: The output decorator.
        :param dl: The metadata layer.
        :param sql_mode: The SQL mode under which the stored routine must be loaded and run.
        :param character_set: The default character set under which the stored routine must be loaded and run.
        :param collate: The default collate under which the stored routine must be loaded and run.
        """
        CommonRoutineLoader.__init__(self, io)

        self._character_set: str = character_set
        """
        The default character set under which the stored routine will be loaded and run.
        """

        self._collate: str = collate
        """
        The default collate under which the stored routine will be loaded and run.
        """

        self._sql_mode: str = sql_mode
        """
        The SQL-mode under which the stored routine will be loaded and run.
        """

        self._dl: MySqlMetadataDataLayer = dl
        """
        The metadata layer.
        """

    # ------------------------------------------------------------------------------------------------------------------
    def _extract_insert_many_table_columns(self, context: LoaderContext) -> None:
        """
        Gets the column names and column types of the current table for bulk insert.

        :param context: The loader context.
        """
        if context.doc_block.designation['type'] != 'insert_many':
            return

        table_name = context.doc_block.designation['table_name']
        keys = context.doc_block.designation['keys']
        is_temporary_table = not self._dl.check_table_exists(table_name)

        if is_temporary_table:
            self._dl.call_stored_routine(context.stored_routine.name)

        rdbms_columns = self._dl.describe_table(table_name)

        if is_temporary_table:
            self._dl.drop_temporary_table(table_name)

        len_keys = len(keys)
        len_columns = len(rdbms_columns)
        if len_columns != len_keys:
            raise LoaderException("Number of keys %d and number of columns %d don't match." % (len_keys, len_columns))

        columns = []
        for rdbms_column in rdbms_columns:
            prog = re.compile(r'(\w+)')
            c_type = prog.findall(rdbms_column['Type'])
            columns.append({'column_name': rdbms_column['Field'],
                            'column_type': c_type[0]})

        context.new_pystratum_metadata['insert_many_columns'] = columns

    # ------------------------------------------------------------------------------------------------------------------
    def _get_data_type_helper(self) -> CommonDataTypeHelper:
        """
        Returns a data type helper object for MySQL.
        """
        return MySqlDataTypeHelper()

    # ------------------------------------------------------------------------------------------------------------------
    def _extract_name(self, context: LoaderContext) -> None:
        """
        Extracts the name of the stored routine and the stored routine type (i.e. procedure or function) source.

        :param context: The loader context.
        """
        prog = re.compile(r"create\s+(procedure|function)\s+([a-z0-9_]+)", re.IGNORECASE)
        matches = prog.findall(context.stored_routine.code)

        if matches and len(matches) == 1:
            context.stored_routine.type = matches[0][0].lower()

            if context.stored_routine.name != matches[0][1]:
                raise LoaderException('Stored routine name {0} does not match filename in file {1}'.
                                      format(matches[0][1], context.stored_routine.path))

        else:
            raise LoaderException('Unable to find the stored routine name and type in file {0}'.
                                  format(context.stored_routine.path))

    # ------------------------------------------------------------------------------------------------------------------
    def _extract_stored_routine_parameters(self, context: LoaderContext) -> None:
        """
        Retrieves the metadata of the stored routine parameters from the MySQL instance.

        :param context: The loader context.
        """
        parameters = []
        routine_parameters = self._dl.get_routine_parameters(context.stored_routine.name)
        for routine_parameter in routine_parameters:
            if routine_parameter['parameter_name']:
                parameter = {'name':      routine_parameter['parameter_name'],
                             'data_type': routine_parameter['parameter_type']}

                if routine_parameter['numeric_precision'] is not None:
                    parameter['numeric_precision'] = routine_parameter['numeric_precision']

                if routine_parameter['numeric_scale'] is not None:
                    parameter['numeric_scale'] = routine_parameter['numeric_scale']

                data_type_descriptor = routine_parameter['column_type']
                if 'character_set_name' in routine_parameter:
                    if routine_parameter['character_set_name']:
                        data_type_descriptor += ' character set %s' % routine_parameter['character_set_name']
                if 'collation' in routine_parameter:
                    if routine_parameter['character_set_name']:
                        data_type_descriptor += ' collation %s' % routine_parameter['collation']
                parameter['data_type_descriptor'] = data_type_descriptor

                parameters.append(parameter)

        context.stored_routine.parameters = parameters

    # ------------------------------------------------------------------------------------------------------------------
    def _load_routine_file(self, context: LoaderContext) -> None:
        """
        Loads the stored routine into the MySQL instance.

        :param context: The loader context.
        """
        self._io.text('Loading {0} <dbo>{1}</dbo>'.format(context.stored_routine.type,
                                                          context.stored_routine.name))

        self._drop_stored_routine(context)

        self._dl.set_sql_mode(self._sql_mode)
        self._dl.set_character_set(self._character_set, self._collate)

        self._dl.execute_none(self._routine_source_code)

    # ------------------------------------------------------------------------------------------------------------------
    def _log_exception(self, exception: Exception) -> None:
        """
        Logs an exception.

        :param exception: The exception.
        """
        CommonRoutineLoader._log_exception(self, exception)

        if isinstance(exception, connector.errors.Error):
            if exception.errno == 1064:
                # Exception is caused by an invalid SQL statement.
                sql = self._dl.last_sql()
                if sql:
                    sql = sql.strip()
                    # The format of a 1064 message is: %s near '%s' at line %d
                    parts = re.search(r'(\d+)$', exception.msg)
                    if parts:
                        error_line = int(parts.group(1))
                    else:
                        error_line = 0

                    self._print_sql_with_error(sql, error_line)

    # ------------------------------------------------------------------------------------------------------------------
    def _must_reload(self, context: LoaderContext) -> bool:
        """
        Returns whether the source file must be load or reloaded.
        """
        if CommonRoutineLoader._must_reload(self, context):
            return True

        if context.old_rdbms_metadata['sql_mode'] != self._sql_mode:
            return True

        if context.old_rdbms_metadata['character_set_client'] != self._character_set:
            return True

        if context.old_rdbms_metadata['collation_connection'] != self._collate:
            return True

        return False

    # ------------------------------------------------------------------------------------------------------------------
    def _drop_stored_routine(self, context: LoaderContext) -> None:
        """
        Drops the stored routine if it exists.

        :param context: The loader context.
        """
        if context.old_rdbms_metadata:
            self._dl.drop_stored_routine(context.old_rdbms_metadata['routine_type'], context.stored_routine.name)

# ----------------------------------------------------------------------------------------------------------------------
