"""核心数据处理模块"""
import os
import math
from mod_config import Config
from mod_logger import Logger
from mod_utils import Utils


class StatsAnalyzer:
    """统计分析类"""
    
    @staticmethod
    def calculate_sum(values):
        """计算求和"""
        return sum(values)
    
    @staticmethod
    def calculate_average(values):
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
        if n % 2 == 1:
            return sorted_values[n // 2]
        else:
            return (sorted_values[n // 2 - 1] + sorted_values[n // 2]) / 2
    
    @staticmethod
    def analyze_data(data):
        """分析数据
        
        参数:
            data: 数据列表
        返回值:
            dict: 统计结果
        """
        values = [item['value'] for item in data]
        
        return {
            'sum': StatsAnalyzer.calculate_sum(values),
            'average': StatsAnalyzer.calculate_average(values),
            'median': StatsAnalyzer.calculate_median(values),
            'count': len(data),
            'min': min(values) if values else 0,
            'max': max(values) if values else 0
        }


class ReportGenerator:
    """报告生成类"""
    
    @staticmethod
    def generate_report(file_info, stats, data_sample):
        """生成报告内容
        
        参数:
            file_info: 文件信息
            stats: 统计结果
            data_sample: 数据样本
        返回值:
            str: 报告内容
        """
        report_lines = []
        report_lines.append(f"# {file_info['name']} 数据报告")
        report_lines.append("")
        report_lines.append("## 文件信息")
        report_lines.append(f"- 文件名: {file_info['name']}")
        report_lines.append(f"- 文件大小: {file_info['size']} 字节")
        report_lines.append(f"- 数据条数: {stats['count']}")
        report_lines.append("")
        
        report_lines.append("## 统计结果")
        report_lines.append("| 指标 | 值 |")
        report_lines.append("|------|----|")
        report_lines.append(f"| 求和 | {stats['sum']:.2f} |")
        report_lines.append(f"| 平均值 | {stats['average']:.2f} |")
        report_lines.append(f"| 中位数 | {stats['median']:.2f} |")
        report_lines.append(f"| 最小值 | {stats['min']:.2f} |")
        report_lines.append(f"| 最大值 | {stats['max']:.2f} |")
        report_lines.append("")
        
        report_lines.append("## 数据样本")
        report_lines.append("| ID | Name | Value |")
        report_lines.append("|----|------|-------|")
        
        sample_size = min(5, len(data_sample))
        for item in data_sample[:sample_size]:
            report_lines.append(f"| {item['id']} | {item['name']} | {item['value']:.2f} |")
        
        if len(data_sample) > sample_size:
            report_lines.append(f"| ... | ... | ... |")
        
        return '\n'.join(report_lines)
    
    @staticmethod
    def save_report(file_path, report_content):
        """保存报告
        
        参数:
            file_path: 原文件路径
            report_content: 报告内容
        """
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        report_file = f"{base_name}_report{Config.REPORT_EXTENSION}"
        report_path = os.path.join(Config.OUTPUT_DIR, report_file)
        
        success = Utils.write_file(report_path, report_content)
        if success:
            Logger.info(f"报告已生成: {report_path}")
        else:
            Logger.error(f"报告生成失败: {report_path}")


class DataProcessor:
    """数据处理类"""
    
    @staticmethod
    def process_file(file_path):
        """处理单个文件
        
        参数:
            file_path: 文件路径
        """
        from mod_validator import DataValidator
        
        Logger.info(f"开始处理文件: {file_path}")
        
        # 验证文件
        is_valid, error_msg, valid_data = DataValidator.validate_file(file_path)
        
        if not is_valid:
            Logger.warning(f"文件验证失败 {file_path}: {error_msg}")
            return False
        
        Logger.info(f"文件验证通过，有效数据条数: {len(valid_data)}")
        
        # 分析数据
        stats = StatsAnalyzer.analyze_data(valid_data)
        Logger.info(f"统计结果: {stats}")
        
        # 获取文件信息
        file_info = Utils.get_file_info(file_path)
        if not file_info:
            Logger.error(f"获取文件信息失败: {file_path}")
            return False
        
        # 生成报告
        report_content = ReportGenerator.generate_report(file_info, stats, valid_data)
        ReportGenerator.save_report(file_path, report_content)
        
        return True
    
    @staticmethod
    def process_directory():
        """处理目录下的所有文件"""
        Logger.info(f"开始处理目录: {Config.INPUT_DIR}")
        
        # 确保目录存在
        if not Utils.ensure_directories():
            Logger.error("目录创建失败")
            return False
        
        # 获取目录下的文件
        files = Utils.get_files_in_directory(Config.INPUT_DIR)
        
        if not files:
            Logger.warning("目录为空")
            return False
        
        # 处理每个文件
        processed_count = 0
        skipped_count = 0
        
        for file_path in files:
            # 检查是否为支持的格式
            if not Utils.is_supported_format(file_path):
                Logger.info(f"跳过不支持的文件: {file_path}")
                skipped_count += 1
                continue
            
            # 处理文件
            if DataProcessor.process_file(file_path):
                processed_count += 1
            else:
                skipped_count += 1
        
        Logger.info(f"处理完成 - 成功: {processed_count}, 跳过: {skipped_count}")
        return True
