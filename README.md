# dataqa-cli

`dataqa-cli` 是一个用于检查 CSV 数据质量的 Python 命令行工具。

这个项目是我的 Python 软件工程学习项目之一，目标是练习文件处理、命令行参数、CSV 数据分析、异常处理和基础数据质量检查能力。项目场景参考 AI 数据标注和数据交付流程中常见的数据质检需求。

## 功能

- 读取指定 CSV 文件
- 输出 CSV 列名
- 输出总数据行数
- 输出总列数
- 统计每一列的空值数量
- 统计每一列的重复值数量
- 预览前 5 行数据
- 处理文件路径缺失和文件不存在等常见错误

## 项目结构

```text
dataqa-cli/
├── csv_profile.py
├── sample.csv
└── README.md
```

## 运行环境

- Python 3.x

本项目当前只使用 Python 标准库，不需要额外安装第三方依赖。

## 使用方法

在项目目录下运行：

```powershell
python .\csv_profile.py .\sample.csv
```

如果没有传入 CSV 文件路径，程序会提示：

```text
请输入 CSV 文件路径
```

如果文件不存在，程序会提示：

```text
文件名错误
```

## 示例输出

```text
列名:['id', 'text', 'label', 'annotator']
总数据行数:8
总列数:4
空值统计:{'id': 0, 'text': 0, 'label': 1, 'annotator': 0}
每一列的重复值数量:{'id': 0, 'text': 1, 'label': 3, 'annotator': 4}
前5行:
{'id': '1', 'text': 'hello world', 'label': 'greeting', 'annotator': 'jjh'}
{'id': '2', 'text': 'python is useful', 'label': 'positive', 'annotator': 'zhc'}
{'id': '3', 'text': 'data quality matters', 'label': 'positive', 'annotator': 'cmd'}
{'id': '4', 'text': 'json parsing failed', 'label': 'negative', 'annotator': 'fsq'}
{'id': '5', 'text': 'fastapi is powerful', 'label': 'positive', 'annotator': 'jjh'}
```

## 核心实现思路

项目使用 Python 标准库中的 `csv.DictReader` 读取 CSV 文件。每一行数据会被解析成字典，列名作为字典的 key。

当前主要包含三个核心函数：

- `analyze_csv_file(file_path)`：读取 CSV 文件，返回列名和数据行。
- `count_empty_values(headers, rows)`：统计每一列的空值数量。
- `count_duplicate_values(headers, rows)`：统计每一列多出来的重复值数量。

## 学习目标

通过这个项目练习：

- Python 函数封装
- 文件读取
- CSV 数据处理
- 字典计数
- 双层循环
- 命令行参数 `sys.argv`
- `try/except` 异常处理
- README 项目说明写法
- Git 和 GitHub 项目管理

## 后续计划

- 支持输出 Markdown 或 HTML 质量报告
- 支持检查指定字段是否为空
- 支持检查标签是否属于允许范围
- 支持统计每一列唯一值数量
- 支持使用 `argparse` 优化命令行参数
- 增加 pytest 单元测试
- 整理为可安装的命令行工具
