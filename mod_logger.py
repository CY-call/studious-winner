#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志记录模块
实现标准化日志输出功能，支持按指定命名生成日志文件
"""

import os
import logging
from datetime import datetime
from mod_config import PathConfig


class Logger:
    """日志记录类"""
    
    _logger = None
    
    @classmethod
    def get_logger(cls):
        """获取日志实例"""
        if cls._logger is None:
            cls._logger = cls._setup_logger()
        return cls._logger
    
    @classmethod
    def _setup_logger(cls):
        """设置日志"""
        logger = logging.getLogger('log_tool')
        logger.setLevel(logging.INFO)
        
        os.makedirs(PathConfig.str_log_dir, exist_ok=True)
        
        str_timestamp = datetime.now().strftime('%Y%m%d')
        str_log_file = os.path.join(
            PathConfig.str_log_dir,
            f'mod_process_{str_timestamp}.log'
        )
        
        file_handler = logging.FileHandler(str_log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    @classmethod
    def info(cls, str_message):
        """记录信息日志"""
        cls.get_logger().info(str_message)
    
    @classmethod
    def warning(cls, str_message):
        """记录警告日志"""
        cls.get_logger().warning(str_message)
    
    @classmethod
    def error(cls, str_message):
        """记录错误日志"""
        cls.get_logger().error(str_message)
    
    @classmethod
    def debug(cls, str_message):
        """记录调试日志"""
        cls.get_logger().debug(str_message)


logger = Logger()
