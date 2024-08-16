#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lixiang
# @File    : readFile.py.py
# @Software: PyCharm

import os,yaml,xlrd
from commons.config.config import CONFIG_PATH, API_YAML_PATH, CONFIG_YAML_PATH
from commons.data.handle_common import extractor, req_expr
from commons.file.handle_system import adjust_path_data
class ReadFile():

    config_dict = None

    @classmethod
    def read_config(cls, file_name, config_path:str=CONFIG_PATH) -> dict:
        # 读取配置文件，并且转换成字典
        """
        :param file_name:
        :param config_path: String类型，配置文件地址，默认使用当前项目目录下的config/config.yaml
        :return: Dict类型，将配置字典返回
        """
        """读取配置文件，并且转换成字典
        :param config_path: 配置文件地址， 默认使用当前项目目录下的config/config.yaml
        return cls.config_dict
        """
        if file_name and config_path:
            # 指定编码格式解决，win下跑代码抛出错误
            with open(os.path.join(config_path, file_name), 'r', encoding='utf-8') as f:
                cls.config_dict = yaml.load(f.read(), Loader=yaml.SafeLoader)
                return cls.config_dict