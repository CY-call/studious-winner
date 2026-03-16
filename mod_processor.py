#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
核心数据处理模块
实现统计分析逻辑，包含数据清洗、求和 / 平均值 / 中位数计算、报告内容组装等核心功能
"""

import os
from datetime import datetime
from  import REPORT_DIR, REPORT_SUFFIX
from  import logger
from  import utils
from  import validator

class StatsAnalyzer:
    @staticmethod
    def calculate_sum(values):
        """计算求和"""
        return sum(values)
    
    @staticmethod
    def calculate_mean(values):
        """计算平均值"""
        if not values:
            return 0
        return sum(values) / len(values)
    
    @staticmethod
    def calculate_median(values):
        """计算中位数"""
        if not values:
            return 0
        sorted_values = sorted(values)
        n = len(sorted_values)
        if n % 2 == 0:
            return (sorted_values[n//2 - 1] + sorted_values[n//2]) / 2
        else:
            return sorted_values[n//2]
    
    def analyze_file(self, file_path):
        """分析单个文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            dict: 分析结果
        """
        try:
            ext = utils.get_file_extension(file_path)
            
            if ext == '.csv':
                data = utils.read_csv_file(file_path)
                is_valid, error_msg, valid_data = validator.validate_csv(file_path, data)
            elif ext == '.json':
                data = utils.read_json_file(file_path)
                is_valid, error_msg, valid_data = validator.validate_json(file_path, data)
            else:
                return {
                    'file': os.path.basename(file_path),
                    'valid': False,
                    'error': '不支持的文件格式'
                }
            
            if not is_valid:
                return {
                    'file': os.path.basename(file_path),
                    'valid': False,
                    'error': error_msg
                }
            
            # 提取数值
            values = [item['value'] for item in valid_data]
            
            # 计算统计指标
            stats = {
                'sum': StatsAnalyzer.calculate_sum(values),
                'mean': StatsAnalyzer.calculate_mean(values),
                'median': StatsAnalyzer.calculate_median(values),
                'count': len(values)
            }
            
            return {
                'file': os.path.basename(file_path),
                'valid': True,
                'data_count': len(valid_data),
                'stats': stats
            }
        except Exception as e:
            error_msg = f"文件分析失败: {str(e)}"
            logger.error(f"{error_msg}, 文件: {file_path}")
            return {
                'file': os.path.basename(file_path),
                'valid': False,
                'error': error_msg
            }

class ReportGenerator:
    @staticmethod
    def generate_report(analysis_results):
        """生成报告
        
        Args:
            analysis_results: 分析结果列表
            
        Returns:
            str: 报告内容
        """
        # 生成报告头部
        report = f"# 数据处理报告\n"
        report += f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # 统计概览
        total_files = len(analysis_results)
        valid_files = sum(1 for r in analysis_results if r['valid'])
        invalid_files = total_files - valid_files
        
        report += f"## 概览\n"
        report += f"- 总文件数: {total_files}\n"
        report += f"- 有效文件数: {valid_files}\n"
        report += f"- 无效文件数: {invalid_files}\n\n"
        
        # 详细统计
        report += "## 详细统计\n"
        
        for result in analysis_results:
            report += f"### {result['file']}\n"
            if result['valid']:
                report += f"- 数据条数: {result['data_count']}\n"
                report += "- 统计指标:\n"
                report += f"  - 求和: {result['stats']['sum']:.2f}\n"
                report += f"  - 平均值: {result['stats']['mean']:.2f}\n"
                report += f"  - 中位数: {result['stats']['median']:.2f}\n"
            else:
                report += f"- 状态: 无效\n"
                report += f"- 错误信息: {result['error']}\n"
            report += "\n"
        
        return report
    
    @staticmethod
    def save_report(report_content):
        """保存报告
        
        Args:
            report_content: 报告内容
            
        Returns:
            str: 报告文件路径
        """
        report_file = os.path.join(REPORT_DIR, f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}{REPORT_SUFFIX}")
        utils.write_file(report_file, report_content)
        return report_file

# 创建实例
analyzer = StatsAnalyzer()
report_generator = ReportGenerator()