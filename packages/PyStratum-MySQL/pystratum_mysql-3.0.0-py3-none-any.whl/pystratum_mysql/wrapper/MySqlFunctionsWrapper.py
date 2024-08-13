from pystratum_common.wrapper.CommonFunctionsWrapper import CommonFunctionsWrapper
from pystratum_common.wrapper.helper import WrapperContext

from pystratum_mysql.wrapper.MySqlWrapper import MySqlWrapper


class MySqlFunctionsWrapper(MySqlWrapper, CommonFunctionsWrapper):
    """
    Wrapper method generator for stored functions.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _build_result_handler(self, context: WrapperContext) -> None:
        """
        Builds the code for calling the stored routine in the wrapper method.

        :param context: The loader context.
        """
        sql = self._generate_command(context.pystratum_metadata)
        if context.pystratum_metadata['pydoc']['return'] == ['bool']:
            statement = f"return self.execute_singleton1({sql}) not in [None, '']"
        else:
            statement = f'return self.execute_singleton1({sql})'
        context.code_store.append_line(statement)

# ----------------------------------------------------------------------------------------------------------------------
