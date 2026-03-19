#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志记录模块
提供统一的日志记录接口，同时输出到文件和控制台
"""

import logging
import os
from mod_config import PathConfig


class Logger:
    """日志类 - 使用PascalCase命名"""
    
    _logger = None
    
    @classmethod
    def get_logger(cls):
        """获取日志实例
        
        返回值:
            logging.Logger: 日志记录器实例
        """
        if cls._logger is None:
            cls._logger = cls._setup_logger()
        return cls._logger
    
    @classmethod
    def _setup_logger(cls):
        """设置日志
        
        返回值:
            logging.Logger: 配置好的日志记录器
        """
        logger = logging.getLogger('log_data_process')
        logger.setLevel(logging.INFO)
        
        # 确保日志目录存在
        os.makedirs(PathConfig.str_log_dir, exist_ok=True)
        
        # 避免重复添加处理器
        if logger.handlers:
            return logger
        
        # 文件处理器
        str_log_file = PathConfig.get_log_file_path()
        file_handler = logging.FileHandler(str_log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 格式化
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加处理器
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    @classmethod
    def info(cls, str_message):
        """记录信息日志
        
        参数:
            str_message: 日志消息
        """
        cls.get_logger().info(str_message)
    
    @classmethod
    def warning(cls, str_message):
        """记录警告日志
        
        参数:
            str_message: 日志消息
        """
        cls.get_logger().warning(str_message)
    
    @classmethod
    def error(cls, str_message):
        """记录错误日志
        
        参数:
            str_message: 日志消息
        """
        cls.get_logger().error(str_message)
    
    @classmethod
    def debug(cls, str_message):
        """记录调试日志
        
        参数:
            str_message: 日志消息
        """
        cls.get_logger().debug(str_message)


# 创建全局日志实例
logger = Logger()
