#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志记录模块
实现标准化日志输出功能，支持按指定命名生成日志文件
"""

import os
import logging
from datetime import datetime
from mod_config import LOG_DIR, LOG_FILE_PREFIX, LOG_LEVEL, ENCODING

class Logger:
    def __init__(self):
        # 确保日志目录存在
        os.makedirs(LOG_DIR, exist_ok=True)
        
        # 生成日志文件名
        today = datetime.now().strftime('%Y%m%d')
        log_file = os.path.join(LOG_DIR, f'{LOG_FILE_PREFIX}_{today}.log')
        
        # 配置日志
        self.logger = logging.getLogger('data_process')
        self.logger.setLevel(getattr(logging, LOG_LEVEL))
        
        # 避免重复添加处理器
        if not self.logger.handlers:
            # 文件处理器
            file_handler = logging.FileHandler(log_file, encoding=ENCODING)
            file_handler.setLevel(getattr(logging, LOG_LEVEL))
            
            # 控制台处理器
            console_handler = logging.StreamHandler()
            console_handler.setLevel(getattr(logging, LOG_LEVEL))
            
            # 日志格式
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            # 添加处理器
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
    
    def get_logger(self):
        """获取日志对象"""
        return self.logger

# 创建全局日志实例
logger = Logger().get_logger()