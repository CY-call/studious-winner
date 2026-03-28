#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用工具函数模块
封装文件读写、数据类型转换、路径校验、日志格式化等通用工具方法
"""

import os
import csv
import json
from mod_config import ENCODING, SUPPORTED_FORMATS
from mod_logger import logger

class Utils:
    @staticmethod
    def read_csv_file(file_path):
        """读取CSV文件"""
        try:
            with open(file_path, 'r', encoding=ENCODING) as f:
                reader = csv.DictReader(f)
                return list(reader)
        except Exception as e:
            logger.error(f"读取CSV文件失败: {file_path}, 错误: {str(e)}")
            raise
    
    @staticmethod
    def read_json_file(file_path):
        """读取JSON文件"""
        try:
            with open(file_path, 'r', encoding=ENCODING) as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"读取JSON文件失败: {file_path}, 错误: {str(e)}")
            raise
    
    @staticmethod
    def write_file(file_path, content):
        """写入文件"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding=ENCODING) as f:
                f.write(content)
            logger.info(f"文件写入成功: {file_path}")
        except Exception as e:
            logger.error(f"文件写入失败: {file_path}, 错误: {str(e)}")
            raise
    
    @staticmethod
    def get_file_extension(file_path):
        """获取文件扩展名"""
        return os.path.splitext(file_path)[1].lower()
    
    @staticmethod
    def is_supported_format(file_path):
        """检查文件格式是否支持"""
        ext = Utils.get_file_extension(file_path)
        return ext in SUPPORTED_FORMATS
    
    @staticmethod
    def is_read_only_file(file_path, read_only_file):
        """检查是否为只读文件"""
        return os.path.abspath(file_path) == os.path.abspath(read_only_file)
    
    @staticmethod
    def safe_float(value):
        """安全转换为浮点数"""
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def ensure_directory(directory):
        """确保目录存在"""
        try:
            os.makedirs(directory, exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"创建目录失败: {directory}, 错误: {str(e)}")
            return False

# 创建工具类实例
utils = Utils()