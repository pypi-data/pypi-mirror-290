from configparser import ConfigParser

from pystratum_backend.StratumIO import StratumIO
from pystratum_common.backend.CommonRoutineWrapperGeneratorWorker import CommonRoutineWrapperGeneratorWorker
from pystratum_common.wrapper.helper import WrapperContext

from pystratum_mysql.backend.MySqlWorker import MySqlWorker
from pystratum_mysql.wrapper import create_routine_wrapper


class MySqlRoutineWrapperGeneratorWorker(MySqlWorker, CommonRoutineWrapperGeneratorWorker):
    """
    Class for generating a class with wrapper methods for calling stored routines in a MySQL database.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, io: StratumIO, config: ConfigParser):
        """
        Object constructor.

        :param io: The output decorator.
        """
        MySqlWorker.__init__(self, io, config)
        CommonRoutineWrapperGeneratorWorker.__init__(self, io, config)

    # ------------------------------------------------------------------------------------------------------------------
    def _build_routine_wrapper(self, context: WrapperContext) -> None:
        """
        Builds a complete wrapper method for a stored routine.

        :param context: The loader context.
        """
        wrapper = create_routine_wrapper(context)
        wrapper.build(context)

# ----------------------------------------------------------------------------------------------------------------------
