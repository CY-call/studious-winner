#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
程序入口文件
负责初始化配置、调用各模块、协调数据处理全流程执行
"""

import os
from mod_config import INPUT_DIR, READ_ONLY_FILE
from mod_logger import logger
from mod_utils import utils
from mod_processor import analyzer, report_generator

class DataProcessTool:
    def __init__(self):
        # 确保必要目录存在
        utils.ensure_directory(INPUT_DIR)
    
    @staticmethod
    def process_files():
        """处理所有文件"""
        logger.info("开始数据处理")
        
        # 获取输入目录下的所有文件
        try:
            files = os.listdir(INPUT_DIR)
        except Exception as e:
            logger.error(f"读取输入目录失败: {str(e)}")
            return False
        
        analysis_results = []
        
        for file_name in files:
            file_path = os.path.join(INPUT_DIR, file_name)
            
            # 跳过目录
            if os.path.isdir(file_path):
                logger.info(f"跳过目录: {file_name}")
                continue
            
            # 检查是否为只读文件
            if utils.is_read_only_file(file_path, READ_ONLY_FILE):
                logger.info(f"跳过只读文件: {file_name}")
                continue
            
            # 检查文件格式
            if not utils.is_supported_format(file_path):
                logger.info(f"跳过不支持的文件格式: {file_name}")
                analysis_results.append({
                    'file': file_name,
                    'valid': False,
                    'error': '不支持的文件格式'
                })
                continue
            
            # 分析文件
            logger.info(f"开始分析文件: {file_name}")
            result = analyzer.analyze_file(file_path)
            analysis_results.append(result)
            
            if result['valid']:
                logger.info(f"文件分析成功: {file_name}")
            else:
                logger.warning(f"文件分析失败: {file_name}, 原因: {result['error']}")
        
        # 生成报告
        logger.info("生成报告")
        report_content = report_generator.generate_report(analysis_results)
        report_file = report_generator.save_report(report_content)
        logger.info(f"报告生成成功: {report_file}")
        
        logger.info("数据处理完成")
        return True

def main():
    """主函数"""
    # 初始化目录
    DataProcessTool()
    # 调用静态方法
    DataProcessTool.process_files()

if __name__ == "__main__":
    main()