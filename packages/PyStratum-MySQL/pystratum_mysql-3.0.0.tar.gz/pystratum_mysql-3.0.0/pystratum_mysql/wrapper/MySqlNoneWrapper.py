from pystratum_common.wrapper.CommonNoneWrapper import CommonNoneWrapper
from pystratum_common.wrapper.helper import WrapperContext

from pystratum_mysql.wrapper.MySqlWrapper import MySqlWrapper


class MySqlNoneWrapper(MySqlWrapper, CommonNoneWrapper):
    """
    Wrapper method generator for stored procedures without any result set.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _build_result_handler(self, context: WrapperContext) -> None:
        """
        Builds the code for calling the stored routine in the wrapper method.

        :param context: The loader context.
        """
        context.code_store.append_line(
                'return self.execute_sp_none({0!s})'.format(self._generate_command(context.pystratum_metadata)))

# ----------------------------------------------------------------------------------------------------------------------
