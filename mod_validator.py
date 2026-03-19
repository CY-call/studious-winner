#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据校验模块
负责校验时间戳、日志级别、日志内容，并进行清洗和格式标准化
"""

import re
from datetime import datetime
from mod_config import obj_validation_config, obj_file_config
from mod_logger import logger
from mod_utils import FileUtils


class LogValidator:
    """日志校验类 - 使用PascalCase命名"""
    
    def __init__(self):
        """初始化校验器"""
        self.str_iso8601_pattern = obj_validation_config.str_iso8601_pattern
        self.lst_common_formats = obj_validation_config.lst_common_formats
        self.str_timestamp_output_format = obj_validation_config.str_timestamp_output_format
        self.lst_valid_levels = obj_validation_config.lst_valid_levels
        self.int_content_min_length = obj_validation_config.int_content_min_length
        self.int_content_max_length = obj_validation_config.int_content_max_length
        self.str_special_chars = obj_validation_config.str_special_chars
        self.re_special_chars = re.compile(f'[{re.escape(self.str_special_chars)}]')
    
    def validate_timestamp(self, str_timestamp):
        """校验并转换时间戳为ISO 8601格式
        
        参数:
            str_timestamp: 原始时间戳
            
        返回值:
            tuple: (是否有效, 转换后的时间戳)
        """
        if not str_timestamp or not str(str_timestamp).strip():
            return False, None
        
        str_ts = str(str_timestamp).strip()
        
        # 检查是否已经是ISO 8601格式
        if re.match(self.str_iso8601_pattern, str_ts):
            try:
                dt = datetime.fromisoformat(str_ts.replace('Z', '+00:00'))
                return True, dt.strftime(self.str_timestamp_output_format)
            except:
                pass
        
        # 尝试使用常见格式解析
        for str_format in self.lst_common_formats:
            try:
                dt = datetime.strptime(str_ts, str_format)
                return True, dt.strftime(self.str_timestamp_output_format)
            except ValueError:
                continue
        
        return False, None
    
    def validate_level(self, str_level):
        """校验日志级别
        
        参数:
            str_level: 原始日志级别
            
        返回值:
            tuple: (是否有效, 标准化后的日志级别)
        """
        if not str_level:
            return False, None
        
        str_level_upper = str(str_level).strip().upper()
        
        if str_level_upper in self.lst_valid_levels:
            return True, str_level_upper
        
        return False, None
    
    def validate_and_clean_content(self, str_content):
        """校验并清洗日志内容
        
        参数:
            str_content: 原始日志内容
            
        返回值:
            tuple: (是否有效, 清洗后的内容)
        """
        if not str_content:
            return False, None
        
        str_clean = str(str_content).strip()
        
        # 长度校验
        if len(str_clean) < self.int_content_min_length or len(str_clean) > self.int_content_max_length:
            return False, None
        
        # 去除特殊字符
        str_clean = self.re_special_chars.sub('', str_clean)
        
        if len(str_clean) < self.int_content_min_length:
            return False, None
        
        return True, str_clean
    
    def validate_record(self, dict_record, str_file_path, int_line_num):
        """校验单条记录
        
        参数:
            dict_record: 记录字典
            str_file_path: 文件路径
            int_line_num: 行号
            
        返回值:
            tuple: (是否有效, 清洗后的记录, 错误信息)
        """
        dict_cleaned = {}
        lst_errors = []
        
        # 校验时间戳
        str_timestamp = dict_record.get('timestamp', '')
        bool_valid_ts, str_cleaned_ts = self.validate_timestamp(str_timestamp)
        if bool_valid_ts:
            dict_cleaned['timestamp'] = str_cleaned_ts
        else:
            lst_errors.append(f'时间戳格式无效: {str_timestamp}')
        
        # 校验日志级别
        str_level = dict_record.get('level', '')
        bool_valid_level, str_cleaned_level = self.validate_level(str_level)
        if bool_valid_level:
            dict_cleaned['level'] = str_cleaned_level
        else:
            lst_errors.append(f'日志级别无效: {str_level}')
        
        # 校验并清洗内容
        str_content = dict_record.get('content', '')
        bool_valid_content, str_cleaned_content = self.validate_and_clean_content(str_content)
        if bool_valid_content:
            dict_cleaned['content'] = str_cleaned_content
        else:
            lst_errors.append(f'内容无效: {str_content}')
        
        if lst_errors:
            str_error_msg = '; '.join(lst_errors)
            logger.warning(f'文件 {str_file_path} 第 {int_line_num} 行校验失败: {str_error_msg}')
            return False, dict_record, str_error_msg
        
        return True, dict_cleaned, ''
    
    def validate_csv_data(self, str_file_path, lst_data):
        """校验CSV数据
        
        参数:
            str_file_path: 文件路径
            lst_data: 数据列表
            
        返回值:
            tuple: (有效数据列表, 无效记录列表)
        """
        lst_valid = []
        lst_invalid = []
        
        if not lst_data:
            return lst_valid, lst_invalid
        
        # 检查列名
        dict_first_row = lst_data[0]
        lst_missing_columns = []
        for str_col in obj_file_config.lst_required_csv_columns:
            if str_col not in dict_first_row:
                lst_missing_columns.append(str_col)
        
        if lst_missing_columns:
            logger.error(f'文件 {str_file_path} 缺少必要列: {", ".join(lst_missing_columns)}')
            return lst_valid, lst_data
        
        # 校验每条记录
        for i, dict_record in enumerate(lst_data, 1):
            bool_valid, dict_result, str_error = self.validate_record(dict_record, str_file_path, i)
            if bool_valid:
                lst_valid.append(dict_result)
            else:
                dict_invalid_record = dict_record.copy()
                dict_invalid_record['_error'] = str_error
                dict_invalid_record['_file'] = str_file_path
                dict_invalid_record['_line'] = i
                lst_invalid.append(dict_invalid_record)
        
        return lst_valid, lst_invalid
    
    def validate_json_data(self, str_file_path, obj_data):
        """校验JSON数据
        
        参数:
            str_file_path: 文件路径
            obj_data: JSON数据
            
        返回值:
            tuple: (有效数据列表, 无效记录列表)
        """
        lst_valid = []
        lst_invalid = []
        
        if obj_data is None:
            return lst_valid, lst_invalid
        
        # 提取数据列表
        if isinstance(obj_data, list):
            lst_items = obj_data
        elif isinstance(obj_data, dict):
            if 'data' in obj_data and isinstance(obj_data['data'], list):
                lst_items = obj_data['data']
            else:
                logger.error(f'文件 {str_file_path} JSON格式不正确，应为列表或包含data字段的字典')
                return lst_valid, lst_invalid
        else:
            logger.error(f'文件 {str_file_path} JSON格式不正确')
            return lst_valid, lst_invalid
        
        # 校验每条记录
        for i, dict_record in enumerate(lst_items, 1):
            if not isinstance(dict_record, dict):
                logger.warning(f'文件 {str_file_path} 第 {i} 项不是字典')
                dict_invalid_record = {'_error': '不是字典格式', '_file': str_file_path, '_line': i}
                lst_invalid.append(dict_invalid_record)
                continue
            
            bool_valid, dict_result, str_error = self.validate_record(dict_record, str_file_path, i)
            if bool_valid:
                lst_valid.append(dict_result)
            else:
                dict_invalid_record = dict_record.copy()
                dict_invalid_record['_error'] = str_error
                dict_invalid_record['_file'] = str_file_path
                dict_invalid_record['_line'] = i
                lst_invalid.append(dict_invalid_record)
        
        return lst_valid, lst_invalid
