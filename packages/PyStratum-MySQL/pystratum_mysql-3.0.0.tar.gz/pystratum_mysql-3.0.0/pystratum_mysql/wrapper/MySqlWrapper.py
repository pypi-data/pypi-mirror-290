from abc import ABC
from typing import Any, Dict

from pystratum_common.wrapper.CommonWrapper import CommonWrapper


class MySqlWrapper(CommonWrapper, ABC):
    """
    Parent class for wrapper method generators for stored procedures and functions.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _generate_command(self, routine: Dict[str, Any]) -> str:
        """
        Generates SQL statement for calling a stored routine.

        :param routine: Metadata of the stored routine.
        """
        parameters = ''
        placeholders = ''

        execute = 'call'
        if routine['designation']['type'] == 'function':
            execute = 'select'

        i = 0
        l = 0
        for parameter in routine['parameters']:
            re_type = self._get_parameter_format_specifier(parameter['data_type'])
            if parameters:
                parameters += ', '
                placeholders += ', '
            parameters += parameter['name']
            placeholders += re_type
            i += 1
            if not re_type == '?':
                l += 1

        if l == 0:
            line = '"{0!s} {1!s}()"'.format(execute, routine['routine_name'])
        elif l >= 1:
            line = '"{0!s} {1!s}({2!s})", {3!s}'.format(execute, routine['routine_name'], placeholders, parameters)
        else:
            raise Exception('Internal error.')

        return line

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _get_parameter_format_specifier(data_type: str) -> str:
        """
        Returns the appropriate format specifier for a parameter type.

        :param data_type: The parameter type.
        """
        lookup = {'bigint':     '%s',
                  'binary':     '%s',
                  'bit':        '%s',
                  'blob':       '%s',
                  'char':       '%s',
                  'date':       '%s',
                  'datetime':   '%s',
                  'decimal':    '%s',
                  'double':     '%s',
                  'enum':       '%s',
                  'float':      '%s',
                  'int':        '%s',
                  'longblob':   '%s',
                  'longtext':   '%s',
                  'mediumblob': '%s',
                  'mediumint':  '%s',
                  'mediumtext': '%s',
                  'set':        '%s',
                  'smallint':   '%s',
                  'text':       '%s',
                  'time':       '%s',
                  'timestamp':  '%s',
                  'tinyblob':   '%s',
                  'tinyint':    '%s',
                  'tinytext':   '%s',
                  'varbinary':  '%s',
                  'varchar':    '%s',
                  'year':       '%s'}

        if data_type in lookup:
            return lookup[data_type]

        raise Exception('Unexpected data type {0!s}.'.format(data_type))

# ----------------------------------------------------------------------------------------------------------------------
