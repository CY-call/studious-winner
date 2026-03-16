"""程序入口文件"""
from mod_config import Config
from mod_logger import Logger
from mod_processor import DataProcessor


def main():
    """主函数"""
    Logger.info("=" * 60)
    Logger.info("数据处理工具启动")
    Logger.info("=" * 60)
    
    try:
        # 处理目录
        success = DataProcessor.process_directory()
        
        if success:
            Logger.info("数据处理完成")
        else:
            Logger.error("数据处理失败")
            
    except Exception as e:
        Logger.error(f"程序执行出错: {e}")
    finally:
        Logger.info("=" * 60)
        Logger.info("数据处理工具结束")
        Logger.info("=" * 60)


if __name__ == "__main__":
    main()
