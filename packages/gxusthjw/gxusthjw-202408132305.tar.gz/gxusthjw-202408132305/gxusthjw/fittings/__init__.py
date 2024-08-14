#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ----------------------------------------------------------------
# File Name:        __init__.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: gxusthjw.fittings包的__init__.py。
#                        承载“拟合”相关的类和函数。
#                   Outer Parameters: xxxxxxx
# Class List:       xxxxxxx
# Function List:    xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2023/10/30     revise
#       Jiwei Huang        0.0.1         2024/08/13     revise
# ----------------------------------------------------------------
# 导包 ============================================================
from .linear_fitting import (linear_fitting_sm_ols,
                             linear_fitting_sm_rlm,
                             LinearFittingMethodOfSm,
                             linear_fitting_sm,
                             interactive_linear_fitting_sm,)

# 声明 ============================================================
__version__ = "0.0.1"

__author__ = "Jiwei Huang"

__doc__ = """
Assembling classes and functions associated with `fitting`.
"""

__all__ = [
    'LinearFittingMethodOfSm',
    'linear_fitting_sm_rlm',
    'linear_fitting_sm_ols',
    'linear_fitting_sm',
    'interactive_linear_fitting_sm',
]
# ==================================================================
