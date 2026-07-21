# dataqa-cli

`dataqa-cli` 是一个用于检查 CSV 数据质量的 Python 命令行工具。

这个项目来自我的 Python 软件工程学习路线，目标是把基础语法练习推进到一个可维护、可测试、可展示的工程项目。项目场景参考 AI 数据标注、数据清洗和数据交付流程中常见的数据质检需求。

## 功能

- 读取指定 CSV 文件
- 输出 CSV 列名
- 输出总数据行数和总列数
- 统计每一列空值数量
- 统计每一列重复值数量
- 统计每一列唯一值数量
- 支持通过 `--preview` 控制预览行数
- 支持通过 `--required` 检查必填字段是否存在或为空
- 支持通过 `--allowed-labels` 检查 `label` 字段中的非法值
- 支持通过 `--output` 生成 Markdown 数据质量报告
- 支持通过 `--json-output` 生成 JSON 数据质量报告
- 处理文件不存在、预览行数为负数等常见错误
- 使用 pytest 覆盖核心函数测试

## 项目结构

```text
dataqa-cli/
├── .gitignore
├── README.md
├── csv_profile.py
├── sample.csv
└── test_csv_profile.py
```

## 运行环境

- Python 3.x
- pytest，用于运行测试

项目主体只使用 Python 标准库；pytest 仅用于测试。

## 快速开始

在项目目录下运行：

```powershell
python .\csv_profile.py .\sample.csv
```

指定预览行数：

```powershell
python .\csv_profile.py .\sample.csv --preview 3
```

生成 Markdown 报告：

```powershell
python .\csv_profile.py .\sample.csv --preview 3 --output report.md
```

生成 JSON 报告：

```powershell
python .\csv_profile.py .\sample.csv --preview 3 --json-output report.json
```

检查必填字段：

```powershell
python .\csv_profile.py .\sample.csv --required label text reviewer
```

这个示例中，如果 CSV 不包含 `reviewer`，程序会将它列为缺失字段；已经存在的 `label` 和 `text` 则会统计各自的空值数量。

必填字段检查也可以与报告输出组合：

```powershell
python .\csv_profile.py .\sample.csv --required label text reviewer --output report.md --json-output report.json
```

检查 `label` 字段的合法值：

```powershell
python .\csv_profile.py .\sample.csv --allowed-labels greeting positive negative
```

同时生成 Markdown 和 JSON 报告：

```powershell
python .\csv_profile.py .\sample.csv --allowed-labels greeting positive negative --output report.md --json-output report.json
```

查看命令帮助：

```powershell
python .\csv_profile.py --help
```

## 示例输出

```text
列名:['id', 'text', 'label', 'annotator']
总数据行数:8
总列数:4
空值统计:{'id': 0, 'text': 0, 'label': 1, 'annotator': 0}
每一列的重复值数量:{'id': 0, 'text': 1, 'label': 3, 'annotator': 4}
前3行预览:
每一列唯一值：{'id': 8, 'text': 7, 'label': 5, 'annotator': 4}
{'id': '1', 'text': 'hello world', 'label': 'greeting', 'annotator': 'jjh'}
{'id': '2', 'text': 'python is useful', 'label': 'positive', 'annotator': 'zhc'}
{'id': '3', 'text': 'data quality matters', 'label': 'positive', 'annotator': 'cmd'}
```

## Markdown 报告示例

使用 `--output report.md` 后会生成类似内容：

```md
# CSV 数据质量报告
- 总数据行数: 8
- 总列数: 4

## 字段统计

| 字段 | 空值数量 | 重复值数量 | 唯一值数量 |
| --- | ---: | ---: | ---: |
| id | 0 | 0 | 8 |
| text | 0 | 1 | 7 |
| label | 1 | 3 | 5 |
| annotator | 0 | 4 | 4 |

## 必填字段检查

- 缺失的必填字段: reviewer

| 必填字段 | 空值数量 |
| --- | ---: |
| label | 1 |
| text | 0 |

## 合法值检查

| 字段 | 字段缺失 | 非法值数量 | 非法值 |
| --- | --- | ---: | --- |
| label | 否 | 2 | neutral |

## 前 3 行预览

- {'id': '1', 'text': 'hello world', 'label': 'greeting', 'annotator': 'jjh'}
```

`report.md` 是本地生成文件，已加入 `.gitignore`，不会提交到仓库。

## JSON 报告示例

使用 `--json-output report.json` 后会生成结构化报告，适合后续被其他程序读取：

```json
{
  "headers": ["id", "text", "label", "annotator"],
  "row_count": 8,
  "column_count": 4,
  "preview": [
    {
      "id": "1",
      "text": "hello world",
      "label": "greeting",
      "annotator": "jjh"
    }
  ],
  "empty_counts": {
    "id": 0,
    "text": 0,
    "label": 1,
    "annotator": 0
  },
  "duplicate_counts": {
    "id": 0,
    "text": 1,
    "label": 3,
    "annotator": 4
  },
  "unique_counts": {
    "id": 8,
    "text": 7,
    "label": 5,
    "annotator": 4
  },
  "allowed_value_validations": {
    "label": {
      "field": "label",
      "missing_field": false,
      "invalid_count": 2,
      "invalid_values": ["neutral"]
    }
  }
}
```

`report.json` 是本地生成文件，已加入 `.gitignore`，不会提交到仓库。

## 测试

运行测试：

```powershell
python -m pytest -v
```

当前测试覆盖：

- CSV 文件读取
- 空值统计
- 空格字符串空值识别
- 重复值统计
- 唯一值统计
- 必填字段存在性和空值校验
- 合法标签校验
- Markdown 报告内容生成
- JSON 报告内容生成

## 核心函数

- `analyze_csv_file(file_path)`：读取 CSV 文件，返回列名和数据行。
- `count_empty_values(headers, rows)`：统计每一列空值数量。
- `count_duplicate_values(headers, rows)`：统计每一列多出来的重复值数量。
- `count_unique_values(headers, rows)`：统计每一列唯一值数量。
- `validate_required_fields(headers, rows, required_fields)`：检查必填字段是否存在并统计空值。
- `validate_allowed_values(headers, rows, field, allowed_values)`：检查字段中的非空值是否合法。
- `build_profile(...)`：汇总全部统计、规则校验和预览结果。
- `build_markdown_report(...)`：生成 Markdown 数据质量报告内容。
- `build_json_report(profile)`：生成 JSON 数据质量报告内容。
- `parse_args()`：解析命令行参数。

## 学习目标

通过这个项目练习：

- Python 函数封装
- 文件读取与 CSV 处理
- 字典和集合式去重思路
- 双层循环处理结构化数据
- `argparse` 命令行参数
- 命令行多值参数 `nargs="*"`
- 使用规则字典配置字段合法值
- `try/except` 异常处理
- Markdown 报告生成
- JSON 报告生成
- pytest 单元测试
- Git 和 GitHub 项目管理

## 后续计划

- 使用表格形式优化 Markdown 报告
- 支持检查指定字段是否为空
- 支持从配置文件读取多字段规则
- 增加 GitHub Actions 自动运行测试
- 整理为可安装的命令行工具
