#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lixiang
# @File    : handle_system.py
# @Software: PyCharm

import os
from common.config.config import CONFIG_PATH, TEST_DATA_PATH

def adjust_path_data(_path):
    """是否自动加入data
    """
    if TEST_DATA_PATH in _path:
        _path = _path
    else:
        _path = os.path.join(TEST_DATA_PATH, _path, )
    return adjust_path(_path)