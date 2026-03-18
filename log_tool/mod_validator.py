#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据校验模块
负责校验时间戳格式、日志级别、日志内容
"""

import re
from datetime import datetime
from mod_config import get_yaml_config
from mod_logger import logger
from mod_utils import FileUtils, DataUtils


class LogValidator:
    """日志校验类"""
    
    def __init__(self):
        """初始化校验器"""
        dict_config = get_yaml_config()
        self.lst_valid_levels = dict_config['valid_levels']
        self.str_iso8601_pattern = dict_config['timestamp']['iso8601_pattern']
        self.lst_common_formats = dict_config['timestamp']['common_formats']
        self.str_output_format = dict_config['timestamp']['output_format']
    
    def validate_timestamp(self, str_timestamp):
        """校验并标准化时间戳"""
        if not str_timestamp or str(str_timestamp).strip() == '':
            return False, None, "时间戳为空"
        
        str_timestamp = str(str_timestamp).strip()
        
        if re.match(self.str_iso8601_pattern, str_timestamp):
            try:
                dt_time = datetime.fromisoformat(str_timestamp.replace('Z', '+00:00'))
                return True, dt_time.strftime(self.str_output_format), None
            except ValueError:
                pass
        
        for str_format in self.lst_common_formats:
            try:
                dt_time = datetime.strptime(str_timestamp, str_format)
                return True, dt_time.strftime(self.str_output_format), None
            except ValueError:
                continue
        
        return False, None, f"无法解析时间戳格式: {str_timestamp}"
    
    def validate_level(self, str_level):
        """校验日志级别"""
        if not str_level or str(str_level).strip() == '':
            return False, None, "日志级别为空"
        
        str_normalized = DataUtils.normalize_level(str_level)
        
        if str_normalized in self.lst_valid_levels:
            return True, str_normalized, None
        else:
            return False, None, f"无效的日志级别: {str_level}"
    
    def validate_content(self, str_content):
        """校验并清洗日志内容"""
        if str_content is None:
            return False, None, "日志内容为空"
        
        str_content = str(str_content).strip()
        
        if not str_content:
            return False, None, "日志内容为空"
        
        str_cleaned = DataUtils.remove_special_chars(str_content)
        
        return True, str_cleaned, None
    
    def validate_record(self, dict_record):
        """校验单条记录"""
        lst_errors = []
        dict_cleaned = {}
        
        if 'timestamp' not in dict_record:
            lst_errors.append("缺少timestamp字段")
        else:
            bool_valid, str_normalized, str_error = self.validate_timestamp(dict_record['timestamp'])
            if bool_valid:
                dict_cleaned['timestamp'] = str_normalized
            else:
                lst_errors.append(str_error)
        
        if 'level' not in dict_record:
            lst_errors.append("缺少level字段")
        else:
            bool_valid, str_normalized, str_error = self.validate_level(dict_record['level'])
            if bool_valid:
                dict_cleaned['level'] = str_normalized
            else:
                lst_errors.append(str_error)
        
        if 'content' not in dict_record:
            lst_errors.append("缺少content字段")
        else:
            bool_valid, str_cleaned, str_error = self.validate_content(dict_record['content'])
            if bool_valid:
                dict_cleaned['content'] = str_cleaned
            else:
                lst_errors.append(str_error)
        
        if lst_errors:
            return False, dict_record, lst_errors
        
        return True, dict_cleaned, None
    
    def validate_file(self, str_file_path):
        """校验文件中的所有记录"""
        lst_valid_records = []
        lst_invalid_records = []
        
        str_ext = str_file_path.lower().split('.')[-1]
        
        if str_ext == 'csv':
            lst_data = FileUtils.read_csv_file(str_file_path)
        elif str_ext == 'json':
            obj_data = FileUtils.read_json_file(str_file_path)
            if isinstance(obj_data, list):
                lst_data = obj_data
            elif isinstance(obj_data, dict) and 'data' in obj_data:
                lst_data = obj_data['data']
            else:
                lst_data = []
        else:
            logger.warning(f"不支持的文件格式: {str_file_path}")
            return lst_valid_records, lst_invalid_records
        
        if not lst_data:
            logger.warning(f"文件为空或读取失败: {str_file_path}")
            return lst_valid_records, lst_invalid_records
        
        for int_idx, dict_record in enumerate(lst_data):
            bool_valid, dict_cleaned, lst_errors = self.validate_record(dict_record)
            
            if bool_valid:
                lst_valid_records.append(dict_cleaned)
            else:
                lst_invalid_records.append({
                    'line': int_idx + 1,
                    'original': dict_record,
                    'errors': lst_errors
                })
        
        logger.info(f"文件 {str_file_path} 校验完成 - 有效: {len(lst_valid_records)}, 无效: {len(lst_invalid_records)}")
        
        return lst_valid_records, lst_invalid_records
