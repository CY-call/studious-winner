#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置项管理模块
统一管理所有路径配置、文件格式规则、统计指标配置等常量
"""

import os
import yaml


class ConfigLoader:
    """配置加载类"""
    
    _config = None
    
    @classmethod
    def load_config(cls, config_path=None):
        """加载配置文件"""
        if cls._config is None:
            if config_path is None:
                config_path = os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    'config.yaml'
                )
            
            with open(config_path, 'r', encoding='utf-8') as f:
                cls._config = yaml.safe_load(f)
        
        return cls._config
    
    @classmethod
    def get_config(cls):
        """获取配置"""
        if cls._config is None:
            cls.load_config()
        return cls._config


class PathConfig:
    """路径配置类 - 使用匈牙利命名法"""
    
    str_base_dir = os.path.dirname(os.path.abspath(__file__))
    str_input_dir = os.path.join(str_base_dir, 'data', 'input')
    str_output_dir = os.path.join(str_base_dir, 'build', 'dist')
    str_log_dir = os.path.join(str_base_dir, 'logs')
    str_legacy_file = os.path.join(str_input_dir, 'legacy.dat')
    str_config_file = os.path.join(str_base_dir, 'config.yaml')


class FileConfig:
    """文件配置类 - 使用匈牙利命名法"""
    
    lst_supported_formats = ['.csv', '.json']
    str_csv_encoding = 'utf-8'
    lst_csv_headers = ['timestamp', 'level', 'content']
    str_json_encoding = 'utf-8'
    int_json_indent = 4


class ValidationConfig:
    """校验配置类 - 使用匈牙利命名法"""
    
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
    str_output_format = '%Y-%m-%dT%H:%M:%S'
    str_special_chars = '~!@#$%^&*()_+{}|:<>?`-=[];\',./'


class AnalysisConfig:
    """分析配置类 - 使用匈牙利命名法"""
    
    int_top_keywords = 10
    int_min_word_length = 2
    lst_stop_words = [
        '的', '是', '在', '有', '和', '了', '不', '这', '我', '他',
        '她', '它', '们', '就', '也', '都', '而', '及', '与', '或',
        'the', 'is', 'at', 'which', 'on', 'and', 'a', 'an', 'to',
        'of', 'in', 'for', 'with', 'as', 'by'
    ]


class OutputConfig:
    """输出配置类 - 使用匈牙利命名法"""
    
    str_report_filename = 'analysis_report.md'
    str_stats_filename = 'summary_stats.json'
    str_invalid_filename = 'invalid_records.json'
    int_json_indent = 4


def get_yaml_config():
    """获取YAML配置"""
    return ConfigLoader.get_config()
