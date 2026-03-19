#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用工具函数模块
封装文件读写、数据类型转换、路径校验等通用工具方法
"""

import os
import csv
import json
from mod_config import PathConfig, FileConfig, OutputConfig
from mod_logger import logger


class FileUtils:
    """文件工具类"""
    
    @staticmethod
    def ensure_directories():
        """确保所有必要的目录存在"""
        try:
            os.makedirs(PathConfig.str_input_dir, exist_ok=True)
            os.makedirs(PathConfig.str_output_dir, exist_ok=True)
            os.makedirs(PathConfig.str_log_dir, exist_ok=True)
            logger.info("目录检查完成")
            return True
        except Exception as e:
            logger.error(f"创建目录失败: {e}")
            return False
    
    @staticmethod
    def get_files_in_directory(str_directory):
        """获取目录下的所有文件"""
        try:
            lst_files = []
            for str_item in os.listdir(str_directory):
                str_item_path = os.path.join(str_directory, str_item)
                if os.path.isfile(str_item_path):
                    lst_files.append(str_item_path)
            return lst_files
        except Exception as e:
            logger.error(f"读取目录失败: {e}")
            return []
    
    @staticmethod
    def is_supported_format(str_file_path):
        """判断文件是否为支持的格式"""
        str_ext = os.path.splitext(str_file_path)[1].lower()
        return str_ext in FileConfig.lst_supported_formats
    
    @staticmethod
    def read_csv_file(str_file_path):
        """读取CSV文件"""
        try:
            lst_data = []
            with open(str_file_path, 'r', encoding=FileConfig.str_csv_encoding) as f:
                obj_reader = csv.DictReader(f)
                for dict_row in obj_reader:
                    lst_data.append(dict_row)
            logger.info(f"成功读取CSV文件: {str_file_path}")
            return lst_data
        except Exception as e:
            logger.error(f"读取CSV文件失败 {str_file_path}: {e}")
            return []
    
    @staticmethod
    def read_json_file(str_file_path):
        """读取JSON文件"""
        try:
            with open(str_file_path, 'r', encoding=OutputConfig.str_json_encoding) as f:
                obj_data = json.load(f)
            logger.info(f"成功读取JSON文件: {str_file_path}")
            return obj_data
        except Exception as e:
            logger.error(f"读取JSON文件失败 {str_file_path}: {e}")
            return None
    
    @staticmethod
    def write_file(str_file_path, str_content):
        """写入文件"""
        try:
            with open(str_file_path, 'w', encoding=OutputConfig.str_json_encoding) as f:
                f.write(str_content)
            logger.info(f"成功写入文件: {str_file_path}")
            return True
        except Exception as e:
            logger.error(f"写入文件失败 {str_file_path}: {e}")
            return False
    
    @staticmethod
    def get_file_info(str_file_path):
        """获取文件信息"""
        try:
            str_file_name = os.path.basename(str_file_path)
            int_file_size = os.path.getsize(str_file_path)
            return {
                'name': str_file_name,
                'path': str_file_path,
                'size': int_file_size
            }
        except Exception as e:
            logger.error(f"获取文件信息失败 {str_file_path}: {e}")
            return None
    
    @staticmethod
    def read_legacy_file(str_file_path):
        """读取legacy.dat文件（只读）"""
        try:
            with open(str_file_path, 'r', encoding=OutputConfig.str_json_encoding) as f:
                str_content = f.read()
            logger.info(f"成功读取legacy文件: {str_file_path}")
            return str_content
        except Exception as e:
            logger.warning(f"读取legacy文件失败 {str_file_path}: {e}")
            return ""


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
