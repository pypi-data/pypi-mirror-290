from typing import Any, Dict, List

from pystratum_common.loader.helper.CommonDataTypeHelper import CommonDataTypeHelper


class MySqlDataTypeHelper(CommonDataTypeHelper):
    """
    Utility class for deriving information based on a MySQL data type.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def all_column_types(self) -> List[str]:
        """
        Returns all column types supported by MySQL.
        """
        return ['int',
                'smallint',
                'tinyint',
                'mediumint',
                'bigint',
                'decimal',
                'float',
                'double',
                'bit',
                'date',
                'datetime',
                'timestamp',
                'time',
                'year',
                'char',
                'varchar',
                'binary',
                'varbinary',
                'enum',
                'set',
                'inet4',
                'inet6',
                'tinyblob',
                'blob',
                'mediumblob',
                'longblob',
                'tinytext',
                'text',
                'mediumtext',
                'longtext']

    # ------------------------------------------------------------------------------------------------------------------
    def column_type_to_python_type(self, data_type_info: Dict[str, Any]) -> str:
        """
        Returns the corresponding Python data type of MySQL data type.

        :param data_type_info: The MySQL data type metadata.
        """
        if data_type_info['data_type'] in ['tinyint',
                                           'smallint',
                                           'mediumint',
                                           'int',
                                           'bigint',
                                           'year',
                                           'bit']:
            return 'int'

        if data_type_info['data_type'] == 'decimal':
            return 'int' if data_type_info['numeric_scale'] == 0 else 'float'

        if data_type_info['data_type'] in ['float',
                                           'double']:
            return 'float'

        if data_type_info['data_type'] in ['char',
                                           'varchar',
                                           'time',
                                           'timestamp',
                                           'date',
                                           'datetime',
                                           'enum',
                                           'set',
                                           'tinytext',
                                           'text',
                                           'mediumtext',
                                           'longtext']:
            return 'str'

        if data_type_info['data_type'] in ['varbinary',
                                           'binary',
                                           'tinyblob',
                                           'blob',
                                           'mediumblob',
                                           'longblob']:
            return 'bytes'

        raise RuntimeError('Unknown data type {0}.'.format(data_type_info['data_type']))

# ----------------------------------------------------------------------------------------------------------------------
