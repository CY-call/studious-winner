#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
程序入口文件
负责初始化配置、调用各模块、协调数据处理全流程执行
"""

from mod_processor import DataProcessor


def main():
    """主函数"""
    obj_processor = DataProcessor()
    obj_processor.process_files()


if __name__ == "__main__":
    main()
