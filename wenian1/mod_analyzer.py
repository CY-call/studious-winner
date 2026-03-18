#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据分析模块
实现日志统计分析功能
"""

import re
from collections import Counter
from datetime import datetime
from mod_config import get_yaml_config, AnalysisConfig
from mod_logger import logger


class DataAnalyzer:
    """数据分析类"""
    
    def __init__(self):
        """初始化分析器"""
        dict_config = get_yaml_config()
        self.int_top_keywords = dict_config['analysis']['top_keywords_count']
        self.int_min_word_length = dict_config['analysis']['min_word_length']
        self.lst_stop_words = set(dict_config['analysis']['stop_words'])
    
    def analyze_by_level(self, lst_records):
        """按日志级别统计数量
        
        参数:
            lst_records: 有效记录列表
        返回值:
            dict: 各级别统计结果
        """
        dict_stats = {}
        
        for dict_record in lst_records:
            str_level = dict_record.get('level', 'UNKNOWN')
            dict_stats[str_level] = dict_stats.get(str_level, 0) + 1
        
        logger.info(f"按级别统计完成: {dict_stats}")
        return dict_stats
    
    def analyze_by_hour(self, lst_records):
        """按小时统计日志产生频次
        
        参数:
            lst_records: 有效记录列表
        返回值:
            dict: 各小时统计结果
        """
        dict_stats = {}
        
        for dict_record in lst_records:
            str_timestamp = dict_record.get('timestamp', '')
            
            if str_timestamp:
                try:
                    dt_time = datetime.strptime(str_timestamp, '%Y-%m-%dT%H:%M:%S')
                    int_hour = dt_time.hour
                    str_hour_key = f"{int_hour:02d}:00-{int_hour+1:02d}:00"
                    dict_stats[str_hour_key] = dict_stats.get(str_hour_key, 0) + 1
                except ValueError:
                    continue
        
        dict_sorted = dict(sorted(dict_stats.items(), key=lambda x: x[0]))
        logger.info(f"按小时统计完成: {len(dict_sorted)} 个时间段")
        return dict_sorted
    
    def extract_keywords(self, lst_records):
        """提取日志内容中出现频率最高的关键词
        
        参数:
            lst_records: 有效记录列表
        返回值:
            list: 前10个高频关键词列表
        """
        lst_all_words = []
        
        for dict_record in lst_records:
            str_content = dict_record.get('content', '')
            
            if not str_content:
                continue
            
            lst_words = self._tokenize(str_content)
            lst_all_words.extend(lst_words)
        
        dict_word_count = Counter(lst_all_words)
        
        lst_top_keywords = dict_word_count.most_common(self.int_top_keywords)
        
        lst_result = [{'keyword': word, 'count': count} for word, count in lst_top_keywords]
        
        logger.info(f"关键词提取完成: {len(lst_result)} 个关键词")
        return lst_result
    
    def _tokenize(self, str_text):
        """分词处理
        
        参数:
            str_text: 文本内容
        返回值:
            list: 分词结果列表
        """
        lst_words = []
        
        lst_chinese_pattern = re.findall(r'[\u4e00-\u9fa5]+', str_text)
        
        for str_chinese in lst_chinese_pattern:
            if len(str_chinese) >= self.int_min_word_length:
                for int_i in range(len(str_chinese) - self.int_min_word_length + 1):
                    str_word = str_chinese[int_i:int_i + self.int_min_word_length]
                    if str_word not in self.lst_stop_words:
                        lst_words.append(str_word)
        
        lst_english_pattern = re.findall(r'[a-zA-Z]+', str_text)
        
        for str_english in lst_english_pattern:
            str_lower = str_english.lower()
            if len(str_lower) >= self.int_min_word_length and str_lower not in self.lst_stop_words:
                lst_words.append(str_lower)
        
        return lst_words
    
    def analyze_all(self, lst_records):
        """执行所有统计分析
        
        参数:
            lst_records: 有效记录列表
        返回值:
            dict: 完整统计结果
        """
        dict_result = {
            'total_records': len(lst_records),
            'level_stats': self.analyze_by_level(lst_records),
            'hourly_stats': self.analyze_by_hour(lst_records),
            'top_keywords': self.extract_keywords(lst_records)
        }
        
        logger.info(f"全部统计分析完成")
        return dict_result
