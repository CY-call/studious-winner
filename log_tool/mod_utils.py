#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用工具函数模块
封装文件读写、数据类型转换、路径校验等通用工具方法
"""

import os
import csv
import json
from mod_config import PathConfig, FileConfig, get_yaml_config
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
                dict_reader = csv.DictReader(f)
                for dict_row in dict_reader:
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
            with open(str_file_path, 'r', encoding=FileConfig.str_csv_encoding) as f:
                obj_data = json.load(f)
            logger.info(f"成功读取JSON文件: {str_file_path}")
            return obj_data
        except Exception as e:
            logger.error(f"读取JSON文件失败 {str_file_path}: {e}")
            return None
    
    @staticmethod
    def write_json_file(str_file_path, obj_data, int_indent=4):
        """写入JSON文件"""
        try:
            with open(str_file_path, 'w', encoding='utf-8') as f:
                json.dump(obj_data, f, ensure_ascii=False, indent=int_indent)
            logger.info(f"成功写入JSON文件: {str_file_path}")
            return True
        except Exception as e:
            logger.error(f"写入JSON文件失败 {str_file_path}: {e}")
            return False
    
    @staticmethod
    def write_file(str_file_path, str_content):
        """写入文件"""
        try:
            with open(str_file_path, 'w', encoding='utf-8') as f:
                f.write(str_content)
            logger.info(f"成功写入文件: {str_file_path}")
            return True
        except Exception as e:
            logger.error(f"写入文件失败 {str_file_path}: {e}")
            return False
    
    @staticmethod
    def read_legacy_file(str_file_path):
        """读取只读文件legacy.dat"""
        try:
            with open(str_file_path, 'r', encoding='utf-8') as f:
                str_content = f.read()
            logger.info(f"成功读取legacy文件: {str_file_path}")
            return str_content
        except Exception as e:
            logger.error(f"读取legacy文件失败 {str_file_path}: {e}")
            return None


class DataUtils:
    """数据工具类"""
    
    @staticmethod
    def safe_float(obj_value):
        """安全转换为浮点数"""
        try:
            return float(obj_value)
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def safe_int(obj_value):
        """安全转换为整数"""
        try:
            return int(obj_value)
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def remove_special_chars(str_content):
        """移除特殊字符"""
        dict_config = get_yaml_config()
        str_special_chars = dict_config['content_filter']['special_chars']
        str_trans_table = str.maketrans('', '', str_special_chars)
        return str_content.translate(str_trans_table)
    
    @staticmethod
    def normalize_level(str_level):
        """标准化日志级别为大写"""
        return str_level.upper().strip()
