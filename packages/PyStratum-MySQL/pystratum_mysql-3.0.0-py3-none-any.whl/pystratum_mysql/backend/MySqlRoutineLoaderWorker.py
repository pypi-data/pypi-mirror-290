from configparser import ConfigParser
from typing import Any, Dict, List

from pystratum_backend.StratumIO import StratumIO
from pystratum_common.backend.CommonRoutineLoaderWorker import CommonRoutineLoaderWorker
from pystratum_common.loader.helper.LoaderContext import LoaderContext

from pystratum_mysql.backend.MySqlWorker import MySqlWorker
from pystratum_mysql.loader.MySqlRoutineLoader import MySqlRoutineLoader


class MySqlRoutineLoaderWorker(MySqlWorker, CommonRoutineLoaderWorker):
    """
    Class for loading stored routines into a MySQL instance from (pseudo) SQL files.
    """
    MAX_LENGTH_CHAR = 255
    """
    Maximum length of a varchar.
    """

    MAX_LENGTH_VARCHAR = 4096
    """
    Maximum length of a varchar.
    """

    MAX_LENGTH_BINARY = 255
    """
    Maximum length of a varbinary.
    """

    MAX_LENGTH_VARBINARY = 4096
    """
    Maximum length of a varbinary.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, io: StratumIO, config: ConfigParser):
        """
        Object constructor.

        :param io: The output decorator.
        """
        MySqlWorker.__init__(self, io, config)
        CommonRoutineLoaderWorker.__init__(self, io, config)

        self.__character_set_client: str | None = None
        """
        The default character set under which the stored routine will be loaded and run.
        """

        self.__collation_connection: str | None = None
        """
        The default collate under which the stored routine will be loaded and run.
        """

        self.__sql_mode: str | None = None
        """
        The SQL mode under which the stored routine will run.
        """

    # ------------------------------------------------------------------------------------------------------------------
    def __save_column_types_exact(self, rows: List[Dict[str, Any]]) -> None:
        """
        Saves the exact column types as replace pairs.

        :param rows: The column types.
        """
        for row in rows:
            hint = row['table_name'] + '.' + row['column_name']

            value = row['column_type']
            if row['character_set_name']:
                value += ' character set ' + row['character_set_name']

            self._add_type_hint(hint, value)

    # ------------------------------------------------------------------------------------------------------------------
    def __save_column_types_max_length(self, rows: List[Dict[str, Any]]) -> None:
        """
        Saves the column types with maximum length as replace pairs.

        :param rows: The column types.
        """
        for row in rows:
            hint = row['table_name'] + '.' + row['column_name'] + '%max'

            if row['data_type'] == 'char':
                value = row['data_type'] + '(' + str(self.MAX_LENGTH_CHAR) + ')'
                value += ' character set ' + row['character_set_name']
                self._add_type_hint(hint, value)

            if row['data_type'] == 'varchar':
                value = row['data_type'] + '(' + str(self.MAX_LENGTH_VARCHAR) + ')'
                value += ' character set ' + row['character_set_name']
                self._add_type_hint(hint, value)

            elif row['data_type'] == 'binary':
                value = row['data_type'] + '(' + str(self.MAX_LENGTH_BINARY) + ')'
                self._add_type_hint(hint, value)

            elif row['data_type'] == 'varbinary':
                value = row['data_type'] + '(' + str(self.MAX_LENGTH_VARBINARY) + ')'
                self._add_type_hint(hint, value)

    # ------------------------------------------------------------------------------------------------------------------
    def _fetch_column_types(self) -> None:
        """
        Selects schema, table, column names and the column type from MySQL and saves them as replace pairs.
        """
        rows = self._dl.get_all_table_columns()
        self.__save_column_types_exact(rows)
        self.__save_column_types_max_length(rows)

        self._io.text('Selected {0} column types for substitution'.format(len(rows)))

    # ------------------------------------------------------------------------------------------------------------------
    def _create_routine_loader(self, context: LoaderContext) -> MySqlRoutineLoader:
        """
        Creates a Routine Loader object.

        :param context: The loader context.
        """
        return MySqlRoutineLoader(self._io,
                                  self._dl,
                                  self.__sql_mode,
                                  self.__character_set_client,
                                  self.__collation_connection)

    # ------------------------------------------------------------------------------------------------------------------
    def _fetch_rdbms_metadata(self) -> List[Dict[str, Any]]:
        """
        Retrieves information about all stored routines in the current schema.
        """
        return self._dl.get_routines()

    # ------------------------------------------------------------------------------------------------------------------
    def _init_rdbms_specific(self) -> None:
        """
        Gets the SQL mode in the order as preferred by MySQL.
        """
        self.__sql_mode = self._dl.get_correct_sql_mode(self.__sql_mode)

    # ------------------------------------------------------------------------------------------------------------------
    def _drop_stored_routine(self, rdbms_metadata: Dict[str, Any]) -> None:
        """
        Drops a stored routine.

        :param rdbms_metadata: The metadata from the RDBMS of the stored routine to be dropped.
        """
        self._dl.drop_stored_routine(rdbms_metadata['routine_type'], rdbms_metadata['routine_name'])

    # ------------------------------------------------------------------------------------------------------------------
    def _read_configuration_file(self) -> None:
        """
        Reads parameters from the configuration file.
        """
        CommonRoutineLoaderWorker._read_configuration_file(self)

        self.__character_set_client = self._config.get('database', 'character_set_client', fallback='utf8mb4')
        self.__collation_connection = self._config.get('database',
                                                       'collation_connection',
                                                       fallback='utf8mb4_general_ci')
        self.__sql_mode = self._config.get('database', 'sql_mode')

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _pystratum_metadata_revision() -> str:
        """
        Returns the revision of the format of the metadata of the stored routines.
        """
        return CommonRoutineLoaderWorker._pystratum_metadata_revision() + '.1'

# ----------------------------------------------------------------------------------------------------------------------
