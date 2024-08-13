from pystratum_common.wrapper.CommonInsertManyWrapper import CommonInsertManyWrapper
from pystratum_common.wrapper.helper import WrapperContext

from pystratum_mysql.wrapper.MySqlWrapper import MySqlWrapper


class MySqlInsertManyWrapper(MySqlWrapper, CommonInsertManyWrapper):
    """
    Wrapper method generator a for a stored procedure that prepares a table to be used with a bulk SQL statement.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _build_result_handler(self, context: WrapperContext) -> None:
        """
        Builds the code for calling the stored routine in the wrapper method.

        :param context: The loader context.
        """
        table_name = context.pystratum_metadata['designation']['table_name']
        keys = context.pystratum_metadata['designation']['keys']
        columns = context.pystratum_metadata['insert_many_columns']

        len_keys = len(keys)
        len_columns = len(columns)
        if len_columns != len_keys:
            raise Exception("Number of keys %d and number of columns %d don't match." % (len_keys, len_columns))

        context.code_store.append_line(f'keys = {str(list(filter(lambda x: x != '_', keys)))}')
        context.code_store.append_line('my_rows = list(tuple(row[key] for key in keys) for row in rows)')

        column_names = []
        values = []
        for index, column in enumerate(columns):
            if keys[index] != '_':
                column_names.append('`' + column['column_name'] + '`')
                values.append('%s')

        sql = 'insert into `{}` ({})\nvalues ({})'.format(table_name, ', '.join(column_names), ', '.join(values))
        context.code_store.append_line(f'sql = """\n{sql}')
        context.code_store.append_line('"""')
        context.code_store.append_line()

        statement = self._generate_command(context.pystratum_metadata)
        context.code_store.append_line('self.execute_sp_none({0!s})'.format(statement))
        context.code_store.append_line()
        context.code_store.append_line('return self.execute_many(sql, my_rows)'.format(statement))

# ----------------------------------------------------------------------------------------------------------------------
