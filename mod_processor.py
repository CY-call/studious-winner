#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
核心数据处理模块
实现数据清洗、统计分析、报告生成等核心功能
"""

import os
from datetime import datetime
from mod_config import PathConfig, obj_output_config
from mod_logger import logger
from mod_utils import FileUtils
from mod_validator import LogValidator
from mod_analyzer import DataAnalyzer


class ReportGenerator:
    """报告生成类 - 使用PascalCase命名"""
    
    @staticmethod
    def generate_markdown_report(dict_stats, lst_invalid_records):
        """生成Markdown格式分析报告
        
        参数:
            dict_stats: 统计数据
            lst_invalid_records: 无效记录列表
            
        返回值:
            str: Markdown报告内容
        """
        lst_lines = []
        lst_lines.append("# 日志数据分析报告")
        lst_lines.append("")
        lst_lines.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lst_lines.append("")
        
        lst_lines.append("## 1. 总体统计")
        lst_lines.append(f"- **总记录数**: {dict_stats['total_records']}")
        lst_lines.append(f"- **无效记录数**: {len(lst_invalid_records)}")
        lst_lines.append("")
        
        lst_lines.append("## 2. 按日志级别统计")
        lst_lines.append("| 日志级别 | 数量 |")
        lst_lines.append("|----------|------|")
        for str_level, int_count in sorted(dict_stats['by_level'].items()):
            lst_lines.append(f"| {str_level} | {int_count} |")
        lst_lines.append("")
        
        lst_lines.append("## 3. 按小时统计")
        lst_lines.append("| 时间段 | 数量 |")
        lst_lines.append("|--------|------|")
        for str_hour, int_count in sorted(dict_stats['by_hour'].items()):
            lst_lines.append(f"| {str_hour} | {int_count} |")
        lst_lines.append("")
        
        lst_lines.append("## 4. Top 10 关键词")
        lst_lines.append("| 排名 | 关键词 | 出现次数 |")
        lst_lines.append("|------|--------|----------|")
        for i, (str_keyword, int_count) in enumerate(dict_stats['top_keywords'], 1):
            lst_lines.append(f"| {i} | {str_keyword} | {int_count} |")
        lst_lines.append("")
        
        if lst_invalid_records:
            lst_lines.append("## 5. 无效记录示例 (前5条)")
            for i, dict_record in enumerate(lst_invalid_records[:5], 1):
                lst_lines.append(f"### 5.{i} 第 {dict_record.get('_line', 'N/A')} 行")
                lst_lines.append(f"- **文件**: {dict_record.get('_file', 'N/A')}")
                lst_lines.append(f"- **错误**: {dict_record.get('_error', 'N/A')}")
                lst_lines.append("")
        
        return '\n'.join(lst_lines)
    
    @staticmethod
    def save_output(dict_stats, lst_invalid_records):
        """保存所有输出文件
        
        参数:
            dict_stats: 统计数据
            lst_invalid_records: 无效记录列表
            
        返回值:
            bool: 是否成功
        """
        bool_success = True
        
        str_markdown_path = os.path.join(PathConfig.str_output_dir, obj_output_config.str_markdown_report)
        str_markdown_content = ReportGenerator.generate_markdown_report(dict_stats, lst_invalid_records)
        if not FileUtils.write_file(str_markdown_path, str_markdown_content):
            bool_success = False
        
        str_stats_path = os.path.join(PathConfig.str_output_dir, obj_output_config.str_summary_stats)
        if not FileUtils.write_json_file(str_stats_path, dict_stats):
            bool_success = False
        
        str_invalid_path = os.path.join(PathConfig.str_output_dir, obj_output_config.str_invalid_records)
        if not FileUtils.write_json_file(str_invalid_path, lst_invalid_records):
            bool_success = False
        
        return bool_success


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
        
        FileUtils.read_legacy_file(PathConfig.str_legacy_file)
        
        lst_files = FileUtils.get_files_in_directory(PathConfig.str_input_dir)
        
        if not lst_files:
            logger.warning("输入目录为空")
            return False
        
        lst_all_valid = []
        lst_all_invalid = []
        
        for str_file_path in lst_files:
            if not FileUtils.is_supported_format(str_file_path):
                logger.info(f"跳过不支持的文件: {str_file_path}")
                continue
            
            logger.info(f"开始处理文件: {str_file_path}")
            
            str_ext = os.path.splitext(str_file_path)[1].lower()
            
            if str_ext == '.csv':
                lst_data = FileUtils.read_csv_file(str_file_path)
                lst_valid, lst_invalid = self.obj_validator.validate_csv_data(str_file_path, lst_data)
            elif str_ext == '.json':
                obj_data = FileUtils.read_json_file(str_file_path)
                lst_valid, lst_invalid = self.obj_validator.validate_json_data(str_file_path, obj_data)
            else:
                continue
            
            lst_all_valid.extend(lst_valid)
            lst_all_invalid.extend(lst_invalid)
            logger.info(f"文件 {str_file_path} 校验完成 - 有效: {len(lst_valid)}, 无效: {len(lst_invalid)}")
        
        logger.info(f"全部文件处理完成 - 有效: {len(lst_all_valid)}, 无效: {len(lst_all_invalid)}")
        
        if not lst_all_valid:
            logger.warning("没有有效数据可供分析")
            return False
        
        dict_stats = self.obj_analyzer.analyze(lst_all_valid)
        
        if not ReportGenerator.save_output(dict_stats, lst_all_invalid):
            logger.error("输出文件保存失败")
            return False
        
        logger.info("=" * 60)
        logger.info("日志数据处理工具结束")
        logger.info("=" * 60)
        
        return True
