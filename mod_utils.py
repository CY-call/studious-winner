#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用工具函数模块
封装文件读写、数据类型转换、路径校验等通用工具方法
"""

import os
import csv
import json
from mod_config import INPUT_DIR, REPORT_DIR, LOG_DIR, SUPPORTED_FORMATS, ENCODING
from mod_logger import logger


class FileUtils:
    """文件工具类"""
    
    @staticmethod
    def ensure_directories():
        """确保所有必要的目录存在"""
        try:
            os.makedirs(INPUT_DIR, exist_ok=True)
            os.makedirs(REPORT_DIR, exist_ok=True)
            os.makedirs(LOG_DIR, exist_ok=True)
            logger.info("目录检查完成")
            return True
        except Exception as e:
            logger.error(f"创建目录失败: {e}")
            return False
    
    @staticmethod
    def get_files_in_directory(directory):
        """获取目录下的所有文件"""
        try:
            files = []
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                if os.path.isfile(item_path):
                    files.append(item_path)
            return files
        except Exception as e:
            logger.error(f"读取目录失败: {e}")
            return []
    
    @staticmethod
    def is_supported_format(file_path):
        """判断文件是否为支持的格式"""
        ext = os.path.splitext(file_path)[1].lower()
        return ext in SUPPORTED_FORMATS
    
    @staticmethod
    def read_csv_file(file_path):
        """读取CSV文件"""
        try:
            data = []
            with open(file_path, 'r', encoding=ENCODING) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
            logger.info(f"成功读取CSV文件: {file_path}")
            return data
        except Exception as e:
            logger.error(f"读取CSV文件失败 {file_path}: {e}")
            return []
    
    @staticmethod
    def read_json_file(file_path):
        """读取JSON文件"""
        try:
            with open(file_path, 'r', encoding=ENCODING) as f:
                data = json.load(f)
            logger.info(f"成功读取JSON文件: {file_path}")
            return data
        except Exception as e:
            logger.error(f"读取JSON文件失败 {file_path}: {e}")
            return None
    
    @staticmethod
    def write_file(file_path, content):
        """写入文件"""
        try:
            with open(file_path, 'w', encoding=ENCODING) as f:
                f.write(content)
            return True
        except Exception as e:
            logger.error(f"写入文件失败 {file_path}: {e}")
            return False
    
    @staticmethod
    def get_file_info(file_path):
        """获取文件信息"""
        try:
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            return {
                'name': file_name,
                'path': file_path,
                'size': file_size
            }
        except Exception as e:
            logger.error(f"获取文件信息失败 {file_path}: {e}")
            return None


class DataUtils:
    """数据工具类"""
    
    @staticmethod
    def safe_float(value):
        """安全转换为浮点数"""
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def safe_int(value):
        """安全转换为整数"""
        try:
            return int(value)
        except (ValueError, TypeError):
            return None
