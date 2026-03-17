#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据格式验证模块
负责校验CSV文件列完整性、JSON文件格式合法性
"""

from mod_config import Config
from mod_logger import logger
from mod_utils import FileUtils, DataUtils


class DataValidator:
    """数据验证类"""
    
    @staticmethod
    def validate_csv(file_path, data):
        """验证CSV文件
        
        参数:
            file_path: 文件路径
            data: 数据列表
        返回值:
            tuple: (是否有效, 错误信息, 有效数据)
        """
        if not data:
            return False, "文件为空", []
        
        # 检查列名
        first_row = data[0]
        missing_columns = []
        for col in Config.REQUIRED_CSV_COLUMNS:
            if col not in first_row:
                missing_columns.append(col)
        
        if missing_columns:
            return False, f"缺少必要列: {', '.join(missing_columns)}", []
        
        # 验证数据
        valid_data = []
        for i, row in enumerate(data):
            row_data = {}
            valid = True
            
            for col in Config.REQUIRED_CSV_COLUMNS:
                value = row.get(col)
                if value is None or str(value).strip() == '':
                    logger.warning(f"文件 {file_path} 第 {i+1} 行缺少 {col} 字段")
                    valid = False
                    break
                
                if col == 'value':
                    float_value = DataUtils.safe_float(value)
                    if float_value is None:
                        logger.warning(f"文件 {file_path} 第 {i+1} 行 value 字段不是有效数字: {value}")
                        valid = False
                        break
                    row_data[col] = float_value
                else:
                    row_data[col] = str(value).strip()
            
            if valid:
                valid_data.append(row_data)
        
        if not valid_data:
            return False, "没有有效的数据行", []
        
        return True, "验证通过", valid_data
    
    @staticmethod
    def validate_json(file_path, data):
        """验证JSON文件
        
        参数:
            file_path: 文件路径
            data: 数据对象
        返回值:
            tuple: (是否有效, 错误信息, 有效数据)
        """
        if data is None:
            return False, "JSON格式错误", []
        
        # 确保是列表或包含数据的字典
        if isinstance(data, list):
            items = data
        elif isinstance(data, dict):
            # 尝试找到数据列表
            if 'data' in data:
                items = data['data']
                if not isinstance(items, list):
                    return False, "JSON中的data字段不是列表", []
            else:
                return False, "JSON缺少data字段", []
        else:
            return False, "JSON格式不正确，应为列表或包含data字段的字典", []
        
        # 验证每个项目
        valid_data = []
        for i, item in enumerate(items):
            if not isinstance(item, dict):
                logger.warning(f"文件 {file_path} 第 {i+1} 项不是字典")
                continue
            
            # 检查必要字段
            if all(key in item for key in ['id', 'name', 'value']):
                float_value = DataUtils.safe_float(item['value'])
                if float_value is not None:
                    valid_item = {
                        'id': str(item['id']),
                        'name': str(item['name']),
                        'value': float_value
                    }
                    valid_data.append(valid_item)
                else:
                    logger.warning(f"文件 {file_path} 第 {i+1} 项 value 不是有效数字")
            else:
                logger.warning(f"文件 {file_path} 第 {i+1} 项缺少必要字段")
        
        if not valid_data:
            return False, "没有有效的数据项", []
        
        return True, "验证通过", valid_data
    
    @staticmethod
    def validate_file(file_path):
        """验证文件
        
        参数:
            file_path: 文件路径
        返回值:
            tuple: (是否有效, 错误信息, 有效数据)
        """
        ext = file_path.lower().split('.')[-1]
        
        if ext == 'csv':
            data = FileUtils.read_csv_file(file_path)
            return DataValidator.validate_csv(file_path, data)
        elif ext == 'json':
            data = FileUtils.read_json_file(file_path)
            return DataValidator.validate_json(file_path, data)
        else:
            return False, "不支持的文件格式", []
