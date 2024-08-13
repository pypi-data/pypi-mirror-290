from pystratum_common.wrapper.CommonRowsWrapper import CommonRowsWrapper
from pystratum_common.wrapper.helper import WrapperContext

from pystratum_mysql.wrapper.MySqlWrapper import MySqlWrapper


class MySqlRowsWrapper(MySqlWrapper, CommonRowsWrapper):
    """
    Wrapper method generator for stored procedures that are selecting 0, 1, or more rows.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _build_result_handler(self, context: WrapperContext) -> None:
        """
        Builds the code for calling the stored routine in the wrapper method.

        :param context: The loader context.
        """
        """
        Generates code for calling the stored routine in the wrapper method.
        """
        context.code_store.append_line(
                'return self.execute_sp_rows({0!s})'.format(self._generate_command(context.pystratum_metadata)))

# ----------------------------------------------------------------------------------------------------------------------
