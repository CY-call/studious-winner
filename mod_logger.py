"""日志记录模块"""
import logging
import os
from datetime import datetime
from mod_config import Config


class Logger:
    """日志类"""
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
        logger = logging.getLogger('data_process')
        logger.setLevel(logging.INFO)
        
        # 确保日志目录存在
        os.makedirs(Config.LOG_DIR, exist_ok=True)
        
        # 生成日志文件名
        timestamp = datetime.now().strftime('%Y%m%d')
        log_file_name = f"{Config.LOG_FILE_PREFIX}{timestamp}{Config.LOG_FILE_EXTENSION}"
        log_file = os.path.join(Config.LOG_DIR, log_file_name)
        
        # 文件处理器
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
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
    def info(cls, message):
        """记录信息日志"""
        cls.get_logger().info(message)
    
    @classmethod
    def warning(cls, message):
        """记录警告日志"""
        cls.get_logger().warning(message)
    
    @classmethod
    def error(cls, message):
        """记录错误日志"""
        cls.get_logger().error(message)
    
    @classmethod
    def debug(cls, message):
        """记录调试日志"""
        cls.get_logger().debug(message)
