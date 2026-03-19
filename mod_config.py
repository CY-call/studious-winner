#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理模块
使用匈牙利命名法，加载config.yaml配置并提供统一访问接口
"""

import os
import yaml
from datetime import datetime


class ConfigLoader:
    """配置加载类"""
    
    @staticmethod
    def load_config(str_config_path):
        """加载YAML配置文件
        
        参数:
            str_config_path: 配置文件路径
            
        返回值:
            dict: 配置字典
        """
        try:
            with open(str_config_path, 'r', encoding='utf-8') as f:
                dict_config = yaml.safe_load(f)
            return dict_config
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return {}


class PathConfig:
    """路径配置类 - 使用匈牙利命名法"""
    
    str_base_dir = os.path.dirname(os.path.abspath(__file__))
    str_input_dir = os.path.join(str_base_dir, 'data', 'input')
    str_output_dir = os.path.join(str_base_dir, 'build', 'dist')
    str_log_dir = os.path.join(str_base_dir, 'logs')
    str_legacy_file = os.path.join(str_input_dir, 'legacy.dat')
    str_config_file = os.path.join(str_base_dir, 'config.yaml')
    
    @classmethod
    def get_log_file_name(cls):
        """获取日志文件名"""
        str_timestamp = datetime.now().strftime('%Y%m%d')
        return f"mod_process_{str_timestamp}.log"
    
    @classmethod
    def get_log_file_path(cls):
        """获取日志文件路径"""
        return os.path.join(cls.str_log_dir, cls.get_log_file_name())


class FileConfig:
    """文件配置类"""
    
    lst_supported_formats = ['.csv', '.json']
    str_csv_encoding = 'utf-8'
    lst_required_csv_columns = ['timestamp', 'level', 'content']
    
    def __init__(self, dict_config):
        """初始化文件配置
        
        参数:
            dict_config: 配置字典
        """
        if dict_config and 'file' in dict_config:
            self.lst_supported_formats = dict_config['file'].get('supported_formats', self.lst_supported_formats)
            self.str_csv_encoding = dict_config['file'].get('csv_encoding', self.str_csv_encoding)
            self.lst_required_csv_columns = dict_config['file'].get('csv_columns', self.lst_required_csv_columns)


class ValidationConfig:
    """校验配置类"""
    
    lst_valid_levels = ['DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL']
    str_iso8601_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})?$'
    lst_common_formats = [
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%dT%H:%M:%S.%f',
        '%Y-%m-%dT%H:%M:%SZ',
        '%Y-%m-%d %H:%M:%S',
        '%Y/%m/%d %H:%M:%S',
        '%d/%m/%Y %H:%M:%S'
    ]
    str_timestamp_output_format = '%Y-%m-%dT%H:%M:%S'
    int_content_min_length = 1
    int_content_max_length = 1000
    str_special_chars = r'~!@#$%^&*()_+{}|:<>?`-=[];'',./'
    
    def __init__(self, dict_config):
        """初始化校验配置
        
        参数:
            dict_config: 配置字典
        """
        if dict_config:
            if 'valid_levels' in dict_config:
                self.lst_valid_levels = dict_config['valid_levels']
            if 'timestamp' in dict_config:
                self.str_iso8601_pattern = dict_config['timestamp'].get('iso8601_pattern', self.str_iso8601_pattern)
                self.lst_common_formats = dict_config['timestamp'].get('common_formats', self.lst_common_formats)
                self.str_timestamp_output_format = dict_config['timestamp'].get('output_format', self.str_timestamp_output_format)
            if 'content' in dict_config:
                self.int_content_min_length = dict_config['content'].get('min_length', self.int_content_min_length)
                self.int_content_max_length = dict_config['content'].get('max_length', self.int_content_max_length)
                self.str_special_chars = dict_config['content'].get('special_chars', self.str_special_chars)


class AnalysisConfig:
    """分析配置类"""
    
    int_top_keywords = 10
    lst_stop_words = []
    
    def __init__(self, dict_config):
        """初始化分析配置
        
        参数:
            dict_config: 配置字典
        """
        if dict_config and 'analysis' in dict_config:
            self.int_top_keywords = dict_config['analysis'].get('top_keywords', self.int_top_keywords)
            self.lst_stop_words = dict_config['analysis'].get('stop_words', self.lst_stop_words)


class OutputConfig:
    """输出配置类"""
    
    str_encoding = 'utf-8'
    int_json_indent = 4
    str_markdown_report = 'analysis_report.md'
    str_summary_stats = 'summary_stats.json'
    str_invalid_records = 'invalid_records.json'
    
    def __init__(self, dict_config):
        """初始化输出配置
        
        参数:
            dict_config: 配置字典
        """
        if dict_config and 'output' in dict_config:
            self.str_encoding = dict_config['output'].get('encoding', self.str_encoding)
            self.int_json_indent = dict_config['output'].get('json_indent', self.int_json_indent)
            self.str_markdown_report = dict_config['output'].get('markdown_report', self.str_markdown_report)
            self.str_summary_stats = dict_config['output'].get('summary_stats', self.str_summary_stats)
            self.str_invalid_records = dict_config['output'].get('invalid_records', self.str_invalid_records)


# 全局配置实例
dict_global_config = ConfigLoader.load_config(PathConfig.str_config_file)
obj_file_config = FileConfig(dict_global_config)
obj_validation_config = ValidationConfig(dict_global_config)
obj_analysis_config = AnalysisConfig(dict_global_config)
obj_output_config = OutputConfig(dict_global_config)
