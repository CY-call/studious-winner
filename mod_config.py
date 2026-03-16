"""配置项管理模块"""
import os
from datetime import datetime


class Config:
    """配置类"""
    # 基础路径
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # 输入输出路径
    INPUT_DIR = os.path.join(BASE_DIR, 'data', 'input')
    OUTPUT_DIR = os.path.join(BASE_DIR, 'build', 'dist')
    LOG_DIR = os.path.join(BASE_DIR, 'logs')
    
    # 特定文件
    LEGACY_FILE = os.path.join(INPUT_DIR, 'legacy.dat')
    
    # 支持的文件格式
    SUPPORTED_FORMATS = ['.csv', '.json']
    
    # 必需的CSV列
    REQUIRED_CSV_COLUMNS = ['id', 'name', 'value']
    
    # 报告格式
    REPORT_EXTENSION = '.md'
    
    # 日志配置
    LOG_FILE_PREFIX = 'mod_process_'
    LOG_FILE_EXTENSION = '.log'
    
    @classmethod
    def get_log_file_name(cls):
        """获取日志文件名"""
        timestamp = datetime.now().strftime('%Y%m%d')
        return f"{cls.LOG_FILE_PREFIX}{timestamp}{cls.LOG_FILE_EXTENSION}"
    
    @classmethod
    def get_log_file_path(cls):
        """获取日志文件路径"""
        return os.path.join(cls.LOG_DIR, cls.get_log_file_name())
