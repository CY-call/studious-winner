#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
程序入口文件
负责初始化配置、调用各模块、协调数据处理全流程执行
"""

from mod_logger import logger
from mod_processor import DataProcessor


def main():
    """主函数"""
    try:
        obj_processor = DataProcessor()
        bool_success = obj_processor.process_files()
        
        if bool_success:
            logger.info("数据处理完成")
        else:
            logger.error("数据处理失败")
            
    except Exception as e:
        logger.error(f"程序执行出错: {e}")


if __name__ == "__main__":
    main()
