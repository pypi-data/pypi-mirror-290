#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lixiang
# @File    : handle_common.py
# @Software: PyCharm

import os
import re
import json
from jsonpath import jsonpath
from loguru import logger
from common.common.constant import Constant
from common.plugin.hooks_plugin import exec_func


def extractor(obj: dict, expr: str = '.', error_flag: bool = False) -> object:
    """
    根据表达式提取字典中的value，表达式, . 提取字典所有内容， $.case 提取一级字典case， $.case.data 提取case字典下的data
    :param obj :json/dict类型数据
    :param expr: 表达式, . 提取字典所有内容， $.case 提取一级字典case， $.case.data 提取case字典下的data
    $.0.1 提取字典中的第一个列表中的第二个的值
    """
    try:
        if isinstance(obj, str):
            obj = json.loads(obj)
        result = jsonpath(obj, expr)[0]
    except Exception as e:
        if error_flag:
            logger.warning(f'{expr} - 提取不到内容！{e}')
        result = expr
    return result

def req_expr(content: str, data: dict = None, expr: str = '\\${(.*?)}', _no_content: int = 0, _dataType:bool=False) -> str:
    """从请求参数的字符串中，使用正则的方法找出合适的字符串内容并进行替换
    :param content: 原始的字符串内容
    :param data: 在该项目中一般为响应字典，从字典取值出来
    :param expr: 查找用的正则表达式
    return content： 替换表达式后的字符串
    """
    if isinstance(content, str):
        content = content.replace('\\', '')
    else:
        content = str(content).replace('\\', '')

    for i in re.findall(expr, content):
        if i.find(".") >= 0:
            from common.plugin.data_bus import DataBus
            _content = DataBus.get_key(i)

        elif get_system_key(f'{i}') is None:
            _content = str(extractor(data, i))
        else:
            _content = get_system_key(f'{i}',_dataType)

        if _content is None or _content == f'{i}':
            if _no_content == 0:
                content = content.replace('${' + f'{i}' + '}', Constant.DATA_NO_CONTENT)
            if _no_content == 1:
                content = content.replace('${' + f'{i}' + '}', f'{i}')
            if _no_content == 2:
                content = content.replace('${' + f'{i}' + '}', '')
            if _no_content == 4:
                content = content.replace(f'{i}', f'{i}')
            if _no_content == 5:
                content1 = {key: val for key, val in convert_json(content).items() if (val != ('${' + f'{i}' + '}'))}
                content = str(content1)
        else:
            content = content.replace('${' + f'{i}' + '}', _content)

        # 增加自定义函数得的调用，函数写在tools/hooks.py中
        for func in re.findall('@(.*?)@', content):
            try:
                content = content.replace(f'@{func}@', exec_func(func))
            except Exception as e:
                logger.error(e)
                continue
    return content

