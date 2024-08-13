from pystratum_common.wrapper.CommonRowsWithKeyWrapper import CommonRowsWithKeyWrapper
from pystratum_common.wrapper.helper import WrapperContext

from pystratum_mysql.wrapper.MySqlWrapper import MySqlWrapper


class MySqlRowsWithKeyWrapper(CommonRowsWithKeyWrapper, MySqlWrapper):
    """
    Wrapper method generator for stored procedures whose result set must be returned using tree structure using a
    combination of unique columns.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _build_execute_rows(self, context: WrapperContext) -> None:
        """
        Builds the code for invoking the stored routine.

        :param context: The loader context.
        """
        context.code_store.append_line(
                'rows = self.execute_sp_rows({0!s})'.format(self._generate_command(context.pystratum_metadata)))

# ----------------------------------------------------------------------------------------------------------------------
