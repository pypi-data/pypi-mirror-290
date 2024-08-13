from pystratum_common.wrapper.CommonRow1Wrapper import CommonRow1Wrapper
from pystratum_common.wrapper.helper import WrapperContext

from pystratum_mysql.wrapper.MySqlWrapper import MySqlWrapper


class MySqlRow1Wrapper(MySqlWrapper, CommonRow1Wrapper):
    """
    Wrapper method generator for stored procedures that are selecting 1 row.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _build_result_handler(self, context: WrapperContext) -> None:
        """
        Builds the code for calling the stored routine in the wrapper method.

        :param context: The loader context.
        """
        context.code_store.append_line(
                'return self.execute_sp_row1({0!s})'.format(self._generate_command(context.pystratum_metadata)))

# ----------------------------------------------------------------------------------------------------------------------
