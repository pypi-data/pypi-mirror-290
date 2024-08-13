from pystratum_common.wrapper.helper import WrapperContext

from pystratum_mysql.wrapper.MySqlBulkWrapper import MySqlBulkWrapper
from pystratum_mysql.wrapper.MySqlFunctionsWrapper import MySqlFunctionsWrapper
from pystratum_mysql.wrapper.MySqlInsertManyWrapper import MySqlInsertManyWrapper
from pystratum_mysql.wrapper.MySqlLogWrapper import MySqlLogWrapper
from pystratum_mysql.wrapper.MySqlMultiWrapper import MySqlMultiWrapper
from pystratum_mysql.wrapper.MySqlNoneWrapper import MySqlNoneWrapper
from pystratum_mysql.wrapper.MySqlRow0Wrapper import MySqlRow0Wrapper
from pystratum_mysql.wrapper.MySqlRow1Wrapper import MySqlRow1Wrapper
from pystratum_mysql.wrapper.MySqlRowsWithIndexWrapper import MySqlRowsWithIndexWrapper
from pystratum_mysql.wrapper.MySqlRowsWithKeyWrapper import MySqlRowsWithKeyWrapper
from pystratum_mysql.wrapper.MySqlRowsWrapper import MySqlRowsWrapper
from pystratum_mysql.wrapper.MySqlSingleton0Wrapper import MySqlSingleton0Wrapper
from pystratum_mysql.wrapper.MySqlSingleton1Wrapper import MySqlSingleton1Wrapper
from pystratum_mysql.wrapper.MySqlWrapper import MySqlWrapper


# ----------------------------------------------------------------------------------------------------------------------

def create_routine_wrapper(context: WrapperContext) -> MySqlWrapper:
    """
    A factory for creating the appropriate object for generating a wrapper method for a stored routine.

    :param context: The loader context.

    :rtype: MySqlWrapper
    """
    designation_type = context.pystratum_metadata['designation']['type']

    if designation_type == 'bulk':
        wrapper = MySqlBulkWrapper()
    elif designation_type == 'insert_many':
        wrapper = MySqlInsertManyWrapper()
    elif designation_type == 'function':
        wrapper = MySqlFunctionsWrapper()
    elif designation_type == 'log':
        wrapper = MySqlLogWrapper()
    elif designation_type == 'multi':
        wrapper = MySqlMultiWrapper()
    elif designation_type == 'none':
        wrapper = MySqlNoneWrapper()
    elif designation_type == 'row0':
        wrapper = MySqlRow0Wrapper()
    elif designation_type == 'row1':
        wrapper = MySqlRow1Wrapper()
    elif designation_type == 'rows_with_index':
        wrapper = MySqlRowsWithIndexWrapper()
    elif designation_type == 'rows_with_key':
        wrapper = MySqlRowsWithKeyWrapper()
    elif designation_type == 'rows':
        wrapper = MySqlRowsWrapper()
    elif designation_type == 'singleton0':
        wrapper = MySqlSingleton0Wrapper()
    elif designation_type == 'singleton1':
        wrapper = MySqlSingleton1Wrapper()
    else:
        raise Exception("Unknown routine type '{0!s}'.".format(designation_type))

    return wrapper

# ----------------------------------------------------------------------------------------------------------------------
