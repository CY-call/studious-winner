"""通用工具函数模块"""
import os
import json
import csv
from mod_config import Config
from mod_logger import Logger


class Utils:
    """工具类"""
    
    @staticmethod
    def ensure_directories():
        """确保所有必要的目录存在"""
        try:
            os.makedirs(Config.INPUT_DIR, exist_ok=True)
            os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
            os.makedirs(Config.LOG_DIR, exist_ok=True)
            return True
        except Exception as e:
            Logger.error(f"创建目录失败: {e}")
            return False
    
    @staticmethod
    def get_files_in_directory(directory):
        """获取目录下的所有文件"""
        try:
            files = []
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                if os.path.isfile(item_path):
                    files.append(item_path)
            return files
        except Exception as e:
            Logger.error(f"读取目录失败: {e}")
            return []
    
    @staticmethod
    def is_supported_format(file_path):
        """判断文件是否为支持的格式"""
        ext = os.path.splitext(file_path)[1].lower()
        return ext in Config.SUPPORTED_FORMATS
    
    @staticmethod
    def read_csv_file(file_path):
        """读取CSV文件"""
        try:
            data = []
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
            return data
        except Exception as e:
            Logger.error(f"读取CSV文件失败 {file_path}: {e}")
            return []
    
    @staticmethod
    def read_json_file(file_path):
        """读取JSON文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except Exception as e:
            Logger.error(f"读取JSON文件失败 {file_path}: {e}")
            return None
    
    @staticmethod
    def write_file(file_path, content):
        """写入文件"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            Logger.error(f"写入文件失败 {file_path}: {e}")
            return False
    
    @staticmethod
    def safe_float(value):
        """安全转换为浮点数"""
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def get_file_info(file_path):
        """获取文件信息"""
        try:
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            return {
                'name': file_name,
                'path': file_path,
                'size': file_size
            }
        except Exception as e:
            Logger.error(f"获取文件信息失败 {file_path}: {e}")
            return None
