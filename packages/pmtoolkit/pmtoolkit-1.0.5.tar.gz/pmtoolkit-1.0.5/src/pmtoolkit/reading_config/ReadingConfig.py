import configparser
import json
import os
from typing import Any, Literal

import xmltodict
import yaml

from pandas import read_excel, read_csv


class ReadingConfig:
    def get(self, input_file: str) -> Any:
        """获取config文件内容

        Args:
            input_file (str): 需要读取的文件路径

        Raises:
            ValueError: 当文件不是.ini/.json/.xml/.yaml的一种时抛出异常

        Returns:
            Any: 依据配置文件类型不同返回字典/字典数组形式
        """
        try:
            os.path.exists(input_file)
        except FileNotFoundError:
            return None
        else:
            file_type = input_file.split('.')[-1]
            # 读取ini
            if file_type == 'ini':
                return self._get_ini(input_file)

            # 读取json
            elif file_type == 'json':
                return self._get_json(input_file)

            # 读取yaml
            elif file_type == 'yaml':
                return self._get_yaml(input_file)

            # 读取xml
            elif file_type == 'xml':
                return self._get_xml(input_file)

            # 读取xlsx
            elif file_type == 'xlsx':
                return self._get_xlsx_to_dict(input_file)

            else:
                raise ValueError(f"Unsupported file type: {file_type}")

    def get_xlsx(self, input_file: str, return_type: Literal['dict', 'array'], header=None) -> Any:
        if return_type == 'dict':
            return self._get_xlsx_to_dict(input_file, header)
        elif return_type == 'array':
            return self._get_xlsx_to_dict(input_file, header)
        else:
            raise ValueError(f"Unsupported return type: {return_type}")

    def get_csv(self, input_file: str, return_type: Literal['dict', 'array'], header=None) -> Any:
        if return_type == 'dict':
            return self._get_csv_to_dict(input_file, header)
        elif return_type == 'array':
            return self._get_csv_to_array(input_file, header)
        else:
            raise ValueError(f"Unsupported return type: {return_type}")

    @staticmethod
    def _get_ini(input_file: str) -> Any:
        """读取ini配置

        Args:
            input_file (str): 需读取文件

        Returns:
           Any: 返回字典类型
        """
        # 创建配置解析器 区分大小写
        config = configparser.RawConfigParser()
        config.optionxform = lambda option: option
        config.read(input_file)

        # 递归返回字典类型
        return {section: dict(config.items(section)) for section in config.sections()}

    @staticmethod
    def _get_json(input_file: str) -> Any:
        """读取json配置

        Args:
            input_file (str): 同_get_ini_

        Returns:
            Any: 返回字典/字典数组类型
        """
        with open(input_file, 'r') as f:
            return json.load(f)

    @staticmethod
    def _get_yaml(input_file: str) -> Any:
        """读取yaml配置

        Args:
            input_file (str): 同_get_ini_

        Returns:
            Any: 返回字典类型
        """
        with open(input_file, 'r') as f:
            return yaml.load(f, Loader=yaml.FullLoader)

    @staticmethod
    def _get_xml(input_file: str) -> Any:
        """读取xml配置

        Args:
            input_file (str): 同_get_ini_

        Returns:
            Any: 返回字典类型
        """
        with open(input_file) as f:
            return xmltodict.parse(f.read())

    @staticmethod
    def _get_xlsx_to_dict(input_file: str, header=0) -> Any:
        file_type = input_file.split('.')[-1]
        if file_type == 'xlsx':
            return read_excel(input_file, header=header, keep_default_na=False, engine='openpyxl').to_dict(
                orient='records')
        elif file_type == 'xls':
            return read_excel(input_file, header=header, keep_default_na=False, engine='xlrd').to_dict(orient='records')
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

    @staticmethod
    def _get_xlsx_to_array(input_file: str, header=None) -> Any:
        file_type = input_file.split('.')[-1]
        if file_type == 'xlsx':
            return read_excel(input_file, header=header, keep_default_na=False, engine='openpyxl').values.tolist()
        elif file_type == 'xls':
            return read_excel(input_file, header=header, keep_default_na=False, engine='xlrd').values.tolist()
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

    @staticmethod
    def _get_csv_to_dict(input_file: str, header=0) -> Any:
        return read_csv(input_file, header=header, keep_default_na=False).to_dict(orient='records')

    @staticmethod
    def _get_csv_to_array(input_file: str, header=None) -> Any:
        return read_csv(input_file, header=header).values.tolist()
