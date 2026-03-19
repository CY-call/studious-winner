#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据分析模块
实现按日志级别统计、按小时统计频次、关键词提取等功能
"""

import re
from datetime import datetime
from collections import Counter
from mod_config import obj_analysis_config
from mod_logger import logger


class DataAnalyzer:
    """数据分析类 - 使用PascalCase命名"""
    
    def __init__(self):
        """初始化分析器"""
        self.int_top_keywords = obj_analysis_config.int_top_keywords
        self.lst_stop_words = obj_analysis_config.lst_stop_words
        self.bool_has_jieba = False
        try:
            import jieba
            self.jieba = jieba
            self.bool_has_jieba = True
        except ImportError:
            logger.warning("jieba未安装，中文分词将使用简单方法")
    
    def count_by_level(self, lst_data):
        """按日志级别统计数量
        
        参数:
            lst_data: 数据列表
            
        返回值:
            dict: 级别统计结果
        """
        dict_level_count = Counter()
        for dict_record in lst_data:
            str_level = dict_record.get('level', '')
            if str_level:
                dict_level_count[str_level] += 1
        logger.info(f"按级别统计完成: {dict(dict_level_count)}")
        return dict(dict_level_count)
    
    def count_by_hour(self, lst_data):
        """按小时统计日志产生频次
        
        参数:
            lst_data: 数据列表
            
        返回值:
            dict: 小时统计结果
        """
        dict_hour_count = Counter()
        for dict_record in lst_data:
            str_timestamp = dict_record.get('timestamp', '')
            if str_timestamp:
                try:
                    dt = datetime.fromisoformat(str_timestamp)
                    str_hour_key = dt.strftime('%Y-%m-%d %H:00')
                    dict_hour_count[str_hour_key] += 1
                except Exception as e:
                    logger.warning(f"解析时间戳失败: {str_timestamp}, 错误: {e}")
        logger.info(f"按小时统计完成: {len(dict_hour_count)} 个时间段")
        return dict(dict_hour_count)
    
    def is_chinese(self, str_text):
        """判断文本是否包含中文
        
        参数:
            str_text: 文本
            
        返回值:
            bool: 是否包含中文
        """
        return bool(re.search(r'[\u4e00-\u9fff]', str_text))
    
    def extract_keywords(self, lst_data):
        """提取日志内容中出现频率最高的关键词
        
        参数:
            lst_data: 数据列表
            
        返回值:
            list: 关键词列表，按频率降序排列
        """
        lst_all_words = []
        
        for dict_record in lst_data:
            str_content = dict_record.get('content', '')
            if not str_content:
                continue
            
            if self.is_chinese(str_content) and self.bool_has_jieba:
                lst_words = self.jieba.lcut(str_content)
            else:
                lst_words = str_content.split()
            
            for str_word in lst_words:
                str_word = str_word.strip().lower()
                if len(str_word) > 1 and str_word not in self.lst_stop_words:
                    lst_all_words.append(str_word)
        
        obj_counter = Counter(lst_all_words)
        lst_top_keywords = obj_counter.most_common(self.int_top_keywords)
        logger.info(f"关键词提取完成: {len(lst_top_keywords)} 个关键词")
        return lst_top_keywords
    
    def analyze(self, lst_data):
        """执行完整分析
        
        参数:
            lst_data: 数据列表
            
        返回值:
            dict: 完整分析结果
        """
        dict_stats = {}
        dict_stats['total_records'] = len(lst_data)
        dict_stats['by_level'] = self.count_by_level(lst_data)
        dict_stats['by_hour'] = self.count_by_hour(lst_data)
        dict_stats['top_keywords'] = self.extract_keywords(lst_data)
        logger.info("全部统计分析完成")
        return dict_stats
