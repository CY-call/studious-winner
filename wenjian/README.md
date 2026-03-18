# studious-winner
测试
你是一个 Python 开发工程师，需要严格按照以下要求编写一个完整可运行的日志数据清洗与分析工具，包含目录自动创建、多格式文件处理、数据校验清洗、统计分析及标准化输出全流程。
任务描述
开发一个自动化日志处理工具，需自动创建指定目录结构，读取./data/input/下的.csv/.json 日志文件，完成数据合法性校验、格式标准化清洗，统计核心指标后，在./build/dist/生成 Markdown 分析报告和 JSON 格式统计文件，全程严格遵守路径、格式、命名等强约束规则。
功能需求
目录自动创建：程序启动时检查并创建./data/input/、./build/dist/目录（不存在则创建）；
文件读取：读取./data/input/下所有.csv/.json 日志文件，忽略其他格式，处理空文件 / 损坏文件异常；
数据校验：
时间戳：校验是否为 ISO 8601 格式，非标准格式自动转换；
日志级别：仅允许 DEBUG/INFO/WARN/ERROR/FATAL，统一转为大写；
日志内容：非空校验，去除特殊字符（~!@#$%^&*()_+{}|:<>?`-=[];',./）；
统计分析：
按日志级别统计数量；
按小时统计日志产生频次；
提取日志内容中出现频率最高的 10 个关键词（中文用 jieba 分词，英文按空格分词）；
输出生成：
./build/dist/analysis_report.md：Markdown 格式分析报告（含标题、表格、列表）；
./build/dist/summary_stats.json：JSON 格式汇总统计数据（格式化输出，indent=4）；
./build/dist/invalid_records.json：JSON 格式校验失败记录清单；
特殊文件处理：读取./data/input/legacy.dat（只读，禁止修改 / 删除），用于参考校验规则。
强约束条件
1. 文件夹路径约束
所有输入必须从./data/input/相对路径读取，输出必须写入./build/dist/相对路径；
禁止使用绝对路径，必须通过os.path模块处理路径拼接；
程序启动时优先校验目录存在性，不存在则自动递归创建；
2. 特定文件格式约束
输入仅处理.csv（UTF-8 编码，表头为 timestamp,level,content）和.json 格式；
输出 Markdown 文件需符合标准语法，JSON 文件需 UTF-8 编码 + 格式化输出；
配置文件config.yaml必须为 YAML 格式，存储校验规则（如合法日志级别、时间戳正则）；
3. 命名规范约束
所有 Python 源码文件必须以mod_开头；
所有类名使用 PascalCase（如LogValidator、DataAnalyzer）；
配置相关变量遵循匈牙利命名法（如str_log_pattern、lst_valid_levels、dict_stats）；
4. 不可修改文件约束
./data/input/legacy.dat为只读文件，仅允许读取，禁止修改 / 删除 / 重命名；
读取该文件时需添加文件锁（跨平台兼容），防止并发写入冲突；
并且你自己创建的文件需要都建在D盘下面，如果文件里面需要填写内容，也需要你自己想内容填写