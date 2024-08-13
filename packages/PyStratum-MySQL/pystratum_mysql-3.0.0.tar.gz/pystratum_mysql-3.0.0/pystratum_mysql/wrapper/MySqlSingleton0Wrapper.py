from pystratum_common.wrapper.CommonSingleton0Wrapper import CommonSingleton0Wrapper
from pystratum_common.wrapper.helper import WrapperContext

from pystratum_mysql.wrapper.MySqlWrapper import MySqlWrapper


class MySqlSingleton0Wrapper(MySqlWrapper, CommonSingleton0Wrapper):
    """
    Wrapper method generator for stored procedures that are selecting 0 or 1 row with one column only.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _build_result_handler(self, context: WrapperContext) -> None:
        """
        Builds the code for calling the stored routine in the wrapper method.

        :param context: The loader context.
        """
        sql = self._generate_command(context.pystratum_metadata)
        if context.pystratum_metadata['pydoc']['return'] == ['bool']:
            statement = f"return self.execute_sp_singleton0({sql}) not in [None, '']"
        else:
            statement = f'return self.execute_sp_singleton0({sql})'
        context.code_store.append_line(statement)

# ----------------------------------------------------------------------------------------------------------------------
