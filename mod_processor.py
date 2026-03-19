#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据处理模块
实现文件处理、报告生成全流程
"""

import json
import os
from mod_config import PathConfig, OutputConfig
from mod_logger import logger
from mod_utils import FileUtils
from mod_validator import LogValidator
from mod_analyzer import DataAnalyzer


class ReportGenerator:
    """报告生成类"""
    
    @staticmethod
    def generate_markdown_report(dict_stats, lst_invalid_records):
        """生成Markdown格式分析报告"""
        lst_lines = []
        
        lst_lines.append("# 日志数据分析报告")
        lst_lines.append("")
        
        lst_lines.append("## 1. 数据概览")
        lst_lines.append("")
        lst_lines.append(f"- **总记录数**: {dict_stats.get('total_records', 0)}")
        lst_lines.append(f"- **有效记录数**: {dict_stats.get('total_records', 0) - len(lst_invalid_records)}")
        lst_lines.append(f"- **无效记录数**: {len(lst_invalid_records)}")
        lst_lines.append("")
        
        lst_lines.append("## 2. 日志级别统计")
        lst_lines.append("")
        lst_lines.append("| 日志级别 | 数量 |")
        lst_lines.append("|----------|------|")
        
        dict_level_stats = dict_stats.get('level_stats', {})
        for str_level, int_count in sorted(dict_level_stats.items(), key=lambda x: x[1], reverse=True):
            lst_lines.append(f"| {str_level} | {int_count} |")
        lst_lines.append("")
        
        lst_lines.append("## 3. 按小时统计")
        lst_lines.append("")
        lst_lines.append("| 时间段 | 日志数量 |")
        lst_lines.append("|--------|----------|")
        
        dict_hourly_stats = dict_stats.get('hourly_stats', {})
        for str_hour, int_count in dict_hourly_stats.items():
            lst_lines.append(f"| {str_hour} | {int_count} |")
        lst_lines.append("")
        
        lst_lines.append("## 4. 高频关键词")
        lst_lines.append("")
        lst_lines.append("| 排名 | 关键词 | 出现次数 |")
        lst_lines.append("|------|--------|----------|")
        
        lst_keywords = dict_stats.get('top_keywords', [])
        for int_idx, dict_keyword in enumerate(lst_keywords, 1):
            lst_lines.append(f"| {int_idx} | {dict_keyword['keyword']} | {dict_keyword['count']} |")
        lst_lines.append("")
        
        if lst_invalid_records:
            lst_lines.append("## 5. 无效记录摘要")
            lst_lines.append("")
            lst_lines.append(f"共有 {len(lst_invalid_records)} 条无效记录，详细信息请查看 invalid_records.json")
            lst_lines.append("")
        
        return '\n'.join(lst_lines)
    
    @staticmethod
    def generate_json_stats(dict_stats):
        """生成JSON格式统计数据"""
        return json.dumps(dict_stats, indent=OutputConfig.int_json_indent, ensure_ascii=False)
    
    @staticmethod
    def generate_invalid_records_json(lst_invalid_records):
        """生成无效记录JSON文件"""
        return json.dumps(lst_invalid_records, indent=OutputConfig.int_json_indent, ensure_ascii=False)


class DataProcessor:
    """数据处理类"""
    
    def __init__(self):
        """初始化处理器"""
        self.obj_validator = LogValidator()
        self.obj_analyzer = DataAnalyzer()
    
    def process_files(self):
        """处理所有文件"""
        logger.info("=" * 60)
        logger.info("日志数据处理工具启动")
        logger.info("=" * 60)
        
        if not FileUtils.ensure_directories():
            logger.error("目录创建失败，程序终止")
            return False
        
        lst_files = FileUtils.get_files_in_directory(PathConfig.str_input_dir)
        
        if not lst_files:
            logger.warning("输入目录为空")
            return False
        
        lst_all_valid_records = []
        lst_all_invalid_records = []
        
        for str_file_path in lst_files:
            if not FileUtils.is_supported_format(str_file_path):
                logger.info(f"跳过不支持的文件: {str_file_path}")
                continue
            
            logger.info(f"开始处理文件: {str_file_path}")
            
            lst_valid, lst_invalid = self.obj_validator.validate_file(str_file_path)
            
            lst_all_valid_records.extend(lst_valid)
            lst_all_invalid_records.extend(lst_invalid)
        
        logger.info(f"全部文件处理完成 - 有效: {len(lst_all_valid_records)}, 无效: {len(lst_all_invalid_records)}")
        
        dict_stats = self.obj_analyzer.analyze_all(lst_all_valid_records)
        
        str_report = ReportGenerator.generate_markdown_report(dict_stats, lst_all_invalid_records)
        str_report_path = os.path.join(PathConfig.str_output_dir, OutputConfig.str_report_filename)
        FileUtils.write_file(str_report_path, str_report)
        
        str_stats_json = ReportGenerator.generate_json_stats(dict_stats)
        str_stats_path = os.path.join(PathConfig.str_output_dir, OutputConfig.str_stats_filename)
        FileUtils.write_file(str_stats_path, str_stats_json)
        
        if lst_all_invalid_records:
            str_invalid_json = ReportGenerator.generate_invalid_records_json(lst_all_invalid_records)
            str_invalid_path = os.path.join(PathConfig.str_output_dir, OutputConfig.str_invalid_filename)
            FileUtils.write_file(str_invalid_path, str_invalid_json)
        
        logger.info("=" * 60)
        logger.info("日志数据处理工具结束")
        logger.info("=" * 60)
        
        return True
