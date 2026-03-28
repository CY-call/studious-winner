#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据格式验证模块
负责校验 CSV 文件列完整性、JSON 文件格式合法性，返回验证结果与错误信息
"""

import json
from mod_config import REQUIRED_CSV_COLUMNS
from mod_logger import logger
from mod_utils import utils

class DataValidator:
    def validate_csv(self, file_path, data):
        """验证CSV文件
        
        Args:
            file_path: 文件路径
            data: CSV数据
            
        Returns:
            tuple: (是否有效, 错误信息, 有效数据)
        """
        try:
            if not data:
                return False, "文件为空", []
            
            # 检查列是否完整
            headers = data[0].keys()
            missing_columns = [col for col in REQUIRED_CSV_COLUMNS if col not in headers]
            if missing_columns:
                return False, f"缺少必要列: {', '.join(missing_columns)}", []
            
            # 提取有效数据
            valid_data = []
            for row in data:
                value = utils.safe_float(row.get('value'))
                if value is not None:
                    valid_data.append({
                        'id': row.get('id'),
                        'name': row.get('name'),
                        'value': value
                    })
            
            if not valid_data:
                return False, "没有有效的数值数据", []
            
            return True, "验证通过", valid_data
        except Exception as e:
            error_msg = f"CSV验证失败: {str(e)}"
            logger.error(f"{error_msg}, 文件: {file_path}")
            return False, error_msg, []
    
    def validate_json(self, file_path, data):
        """验证JSON文件
        
        Args:
            file_path: 文件路径
            data: JSON数据
            
        Returns:
            tuple: (是否有效, 错误信息, 有效数据)
        """
        try:
            if not data:
                return False, "文件为空", []
            
            # 检查数据结构
            if isinstance(data, list):
                # 列表形式
                valid_data = []
                for item in data:
                    if isinstance(item, dict):
                        value = utils.safe_float(item.get('value'))
                        if value is not None:
                            valid_data.append({
                                'id': item.get('id'),
                                'name': item.get('name'),
                                'value': value
                            })
            elif isinstance(data, dict):
                # 字典形式
                valid_data = []
                # 尝试从常见键中提取数据
                for key in ['data', 'items', 'records']:
                    if key in data and isinstance(data[key], list):
                        for item in data[key]:
                            if isinstance(item, dict):
                                value = utils.safe_float(item.get('value'))
                                if value is not None:
                                    valid_data.append({
                                        'id': item.get('id'),
                                        'name': item.get('name'),
                                        'value': value
                                    })
                        break
                # 如果没有找到标准结构，尝试直接解析
                if not valid_data:
                    value = utils.safe_float(data.get('value'))
                    if value is not None:
                        valid_data.append({
                            'id': data.get('id'),
                            'name': data.get('name'),
                            'value': value
                        })
            else:
                return False, "JSON格式不正确", []
            
            if not valid_data:
                return False, "没有有效的数值数据", []
            
            return True, "验证通过", valid_data
        except Exception as e:
            error_msg = f"JSON验证失败: {str(e)}"
            logger.error(f"{error_msg}, 文件: {file_path}")
            return False, error_msg, []

# 创建验证器实例
validator = DataValidator()