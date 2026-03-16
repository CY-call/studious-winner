#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置项管理模块
统一管理所有路径配置、文件格式规则、统计指标配置等常量
"""

import os

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# 输入数据目录
INPUT_DIR = os.path.join(PROJECT_ROOT, 'data', 'input')

# 输出报告目录
REPORT_DIR = os.path.join(PROJECT_ROOT, 'build', 'dist')

# 日志存储目录
LOG_DIR = os.path.join(PROJECT_ROOT, 'logs')

# 支持的文件格式
SUPPORTED_FORMATS = ['.csv', '.json']

# CSV文件必须包含的列
REQUIRED_CSV_COLUMNS = ['id', 'name', 'value']

# 统计指标配置
STATISTICAL_METRICS = {
    'sum': '求和',
    'mean': '平均值',
    'median': '中位数'
}

# 只读文件
READ_ONLY_FILE = os.path.join(INPUT_DIR, 'legacy.dat')

# 日志文件命名前缀
LOG_FILE_PREFIX = 'mod_process'

# 日志级别
LOG_LEVEL = 'INFO'

# 报告文件后缀
REPORT_SUFFIX = '.md'

# 编码格式
ENCODING = 'utf-8'