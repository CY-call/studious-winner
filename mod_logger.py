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
    
    def __init__(self):
        """初始化日志记录器"""
        os.makedirs(PathConfig.str_log_dir, exist_ok=True)
        
        str_today = datetime.now().strftime('%Y%m%d')
        str_log_file = os.path.join(PathConfig.str_log_dir, f'log_{str_today}.log')
        
        self.logger = logging.getLogger('data_process')
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            obj_file_handler = logging.FileHandler(str_log_file, encoding='utf-8')
            obj_file_handler.setLevel(logging.INFO)
            
            obj_console_handler = logging.StreamHandler()
            obj_console_handler.setLevel(logging.INFO)
            
            str_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            obj_file_handler.setFormatter(str_formatter)
            obj_console_handler.setFormatter(str_formatter)
            
            self.logger.addHandler(obj_file_handler)
            self.logger.addHandler(obj_console_handler)
    
    def info(self, str_msg):
        """记录INFO级别日志"""
        self.logger.info(str_msg)
    
    def error(self, str_msg):
        """记录ERROR级别日志"""
        self.logger.error(str_msg)
    
    def warning(self, str_msg):
        """记录WARNING级别日志"""
        self.logger.warning(str_msg)
    
    def debug(self, str_msg):
        """记录DEBUG级别日志"""
        self.logger.debug(str_msg)


logger = Logger()
