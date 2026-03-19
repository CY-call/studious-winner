#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据校验模块
负责校验时间戳格式、日志级别、日志内容
"""

import re
from datetime import datetime
from mod_config import PathConfig, FileConfig, ValidationConfig
from mod_logger import logger
from mod_utils import FileUtils


class LogValidator:
    """日志校验类"""
    
    def __init__(self):
        """初始化校验器"""
        self.lst_valid_levels = ValidationConfig.lst_valid_levels
        self.lst_common_formats = ValidationConfig.lst_common_formats
        self.str_output_format = ValidationConfig.str_output_format
        self.str_special_chars = ValidationConfig.str_special_chars
        self.re_special_chars = re.compile(f'[{re.escape(self.str_special_chars)}]')
    
    def validate_timestamp(self, str_timestamp):
        """校验并转换时间戳"""
        if not str_timestamp:
            return None
        
        str_ts = str(str_timestamp).strip()
        
        for str_format in self.lst_common_formats:
            try:
                dt = datetime.strptime(str_ts, str_format)
                return dt.strftime(self.str_output_format)
            except ValueError:
                continue
        
        return None
    
    def validate_level(self, str_level):
        """校验日志级别"""
        if not str_level:
            return None
        
        str_level_upper = str(str_level).strip().upper()
        
        if str_level_upper in self.lst_valid_levels:
            return str_level_upper
        
        return None
    
    def validate_content(self, str_content):
        """校验并清洗日志内容"""
        if not str_content:
            return None
        
        str_clean = str(str_content).strip()
        
        if len(str_clean) < 1:
            return None
        
        str_clean = self.re_special_chars.sub('', str_clean)
        
        if len(str_clean) < 1:
            return None
        
        return str_clean
    
    def validate_record(self, dict_record, str_file_path, int_line_num):
        """校验单条记录"""
        dict_cleaned = {}
        lst_errors = []
        
        str_timestamp = dict_record.get('timestamp', '')
        str_cleaned_ts = self.validate_timestamp(str_timestamp)
        if str_cleaned_ts:
            dict_cleaned['timestamp'] = str_cleaned_ts
        else:
            lst_errors.append(f'时间戳格式无效: {str_timestamp}')
        
        str_level = dict_record.get('level', '')
        str_cleaned_level = self.validate_level(str_level)
        if str_cleaned_level:
            dict_cleaned['level'] = str_cleaned_level
        else:
            lst_errors.append(f'日志级别无效: {str_level}')
        
        str_content = dict_record.get('content', '')
        str_cleaned_content = self.validate_content(str_content)
        if str_cleaned_content:
            dict_cleaned['content'] = str_cleaned_content
        else:
            lst_errors.append(f'内容无效: {str_content}')
        
        if lst_errors:
            str_error_msg = '; '.join(lst_errors)
            logger.warning(f'文件 {str_file_path} 第 {int_line_num} 行校验失败: {str_error_msg}')
            return False, dict_record, str_error_msg
        
        return True, dict_cleaned, ''
    
    def validate_file(self, str_file_path):
        """校验文件"""
        lst_valid_records = []
        lst_invalid_records = []
        
        str_ext = str_file_path.lower().split('.')[-1]
        
        if str_ext == 'csv':
            lst_data = FileUtils.read_csv_file(str_file_path)
            if not lst_data:
                return lst_valid_records, lst_invalid_records
            
            dict_first_row = lst_data[0]
            lst_missing_columns = []
            for str_col in FileConfig.lst_csv_headers:
                if str_col not in dict_first_row:
                    lst_missing_columns.append(str_col)
            
            if lst_missing_columns:
                logger.error(f'文件 {str_file_path} 缺少必要列: {", ".join(lst_missing_columns)}')
                return lst_valid_records, lst_invalid_records
            
            for i, dict_record in enumerate(lst_data, 1):
                bool_valid, dict_result, str_error = self.validate_record(dict_record, str_file_path, i)
                if bool_valid:
                    lst_valid_records.append(dict_result)
                else:
                    dict_invalid_record = dict_record.copy()
                    dict_invalid_record['_error'] = str_error
                    dict_invalid_record['_file'] = str_file_path
                    dict_invalid_record['_line'] = i
                    lst_invalid_records.append(dict_invalid_record)
        
        elif str_ext == 'json':
            obj_data = FileUtils.read_json_file(str_file_path)
            if obj_data is None:
                return lst_valid_records, lst_invalid_records
            
            if isinstance(obj_data, list):
                lst_items = obj_data
            elif isinstance(obj_data, dict):
                if 'data' in obj_data and isinstance(obj_data['data'], list):
                    lst_items = obj_data['data']
                else:
                    logger.error(f'文件 {str_file_path} JSON格式不正确')
                    return lst_valid_records, lst_invalid_records
            else:
                logger.error(f'文件 {str_file_path} JSON格式不正确')
                return lst_valid_records, lst_invalid_records
            
            for i, dict_record in enumerate(lst_items, 1):
                if not isinstance(dict_record, dict):
                    continue
                
                bool_valid, dict_result, str_error = self.validate_record(dict_record, str_file_path, i)
                if bool_valid:
                    lst_valid_records.append(dict_result)
                else:
                    dict_invalid_record = dict_record.copy()
                    dict_invalid_record['_error'] = str_error
                    dict_invalid_record['_file'] = str_file_path
                    dict_invalid_record['_line'] = i
                    lst_invalid_records.append(dict_invalid_record)
        
        logger.info(f"文件 {str_file_path} 校验完成 - 有效: {len(lst_valid_records)}, 无效: {len(lst_invalid_records)}")
        
        return lst_valid_records, lst_invalid_records
