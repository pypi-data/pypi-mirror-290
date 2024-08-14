#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ----------------------------------------------------------------
# File Name:        __init__.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: gxusthjw.commons包的__init__.py。
#                                  承载“常见的”函数和类。
#                   Outer Parameters: xxxxxxx
# Class List:       xxxxxxx
# Function List:    xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2023/10/30     revise
#       Jiwei Huang        0.0.1         2024/08/12     revise
# ----------------------------------------------------------------
# 导包 ============================================================
from .file_object import (get_file_encoding_chardet,
                          file_info,
                          get_file_info,
                          get_file_info_of_module,
                          get_file_object,
                          FileInfo,
                          FileObject)
from .unique_object import (random_string,
                            unique_string,
                            UniqueObject)
from .str_utils import (str_partition, )
from .math_plus import (traditional_round, )
from .numpy_plus import (traditional_round_np, sech_np, sech,
                         coth_np, coth, cech_np, cech)

# 声明 ============================================================
__version__ = "0.0.1"

__author__ = "Jiwei Huang"

__doc__ = """
The common functions and classes of the gxusthjw python libraries.
"""

__all__ = [
    'get_file_encoding_chardet',
    'file_info',
    'get_file_info',
    'get_file_info_of_module',
    'get_file_object',
    'FileInfo',
    'FileObject',
    'random_string',
    'unique_string',
    'UniqueObject',
    'str_partition',
    'traditional_round',
    'traditional_round_np',
    'sech_np',
    'sech',
    'coth_np',
    'coth',
    'cech_np',
    'cech',
]
# ==================================================================
