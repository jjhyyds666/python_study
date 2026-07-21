import argparse
import csv
import json
import sys


def analyze_csv_file(file_path):
    """读取 CSV 文件，返回表头列表和每一行组成的字典列表。"""
    with open(file_path, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames
        rows = list(reader)

    return headers, rows


def count_empty_values(headers, rows):
    """统计每一列中空字符串或只包含空格的值数量。"""
    empty_counts = {}

    for header in headers:
        empty_counts[header] = 0

    for row in rows:
        for header in headers:
            if row[header].strip() == "":
                empty_counts[header] += 1

    return empty_counts


def count_duplicate_values(headers, rows):
    """统计每一列中重复出现的值数量，只计算第一次出现之后的重复项。"""
    duplicate_counts = {}

    for header in headers:
        seen_values = {}
        duplicate_counts[header] = 0

        for row in rows:
            value = row[header].strip()

            if value not in seen_values:
                seen_values[value] = 0
            else:
                seen_values[value] += 1
                duplicate_counts[header] += 1

    return duplicate_counts


def parse_args():
    """解析命令行参数，并检查 preview 参数不能为负数。"""
    parser = argparse.ArgumentParser(description="检查 CSV 文件的数据质量")
    parser.add_argument("file_path", help="要检查的 CSV 文件路径")
    parser.add_argument(
        "--preview",
        type=int,
        default=5,
        help="预览前 N 行数据，默认 5 行",
    )
    parser.add_argument("--output", help="将 Markdown 报告写入指定文件")
    parser.add_argument("--json-output", help="将 JSON 报告写入指定文件")

    args = parser.parse_args()

    if args.preview < 0:
        parser.error("--preview 不能是负数")

    return args


def count_unique_values(headers, rows):
    """统计每一列去重后的唯一值数量。"""
    unique_counts = {}

    for header in headers:
        values = set()

        for row in rows:
            values.add(row[header].strip())

        unique_counts[header] = len(values)

    return unique_counts


def build_markdown_report(profile):
    """根据数据画像 profile 生成 Markdown 格式的数据质量报告。"""
    lines = []
    lines.append("# CSV 数据质量报告")
    lines.append(f"- 总数据行数: {profile['row_count']}")
    lines.append(f"- 总列数: {profile['column_count']}")

    lines.append("")
    lines.append("## 字段统计")
    lines.append("")
    lines.append("| 字段 | 空值数量 | 重复值数量 | 唯一值数量 |")
    lines.append("| --- | ---: | ---: | ---: |")

    for header in profile["headers"]:
        lines.append(
            f"| {header} | {profile['empty_counts'][header]} | "
            f"{profile['duplicate_counts'][header]} | "
            f"{profile['unique_counts'][header]} |"
        )

    lines.append("")
    lines.append(f"## 前 {len(profile['preview'])} 行预览")
    lines.append("")

    for row in profile["preview"]:
        lines.append(f"- {row}")

    return "\n".join(lines)


def build_profile(headers, rows, preview):
    """汇总 CSV 的基础信息、字段统计和预览数据。"""
    return {
        "headers": headers,
        "row_count": len(rows),
        "column_count": len(headers),
        "preview": rows[:preview],
        "empty_counts": count_empty_values(headers, rows),
        "duplicate_counts": count_duplicate_values(headers, rows),
        "unique_counts": count_unique_values(headers, rows),
    }


def print_profile(profile):
    """将数据画像的主要统计结果打印到命令行。"""
    print(f"列名:{profile['headers']}")
    print(f"总数据行数:{profile['row_count']}")
    print(f"总列数:{profile['column_count']}")
    print(f"空值统计:{profile['empty_counts']}")
    print(f"每一列的重复值数量:{profile['duplicate_counts']}")
    print(f"每一列唯一值：{profile['unique_counts']}")
    for row in profile["preview"]:
        print(row)


def build_json_report(profile):
    """根据数据画像 profile 生成格式化后的 JSON 字符串。"""
    return json.dumps(profile, ensure_ascii=False, indent=2)


def validate_required_fields(headers, rows, required_fields):
    """检查必填字段是否存在，并统计已存在必填字段的空值数量。"""
    return_required = {
        "missing_fields": [],
        "empty_required_counts": {},
    }

    for required_field in required_fields:
        if required_field not in headers:
            return_required["missing_fields"].append(required_field)
        else:
            return_required["empty_required_counts"][required_field] = 0

    for empty_required in return_required["empty_required_counts"]:
        for row in rows:
            if row[empty_required].strip() == "":
                return_required["empty_required_counts"][empty_required] += 1

    return return_required


def main():
    """程序入口：读取参数、分析 CSV，并按需输出 Markdown 或 JSON 报告。"""
    args = parse_args()
    file_path = args.file_path
    preview = args.preview
    output_path = args.output
    json_output_path = args.json_output
    try:
        headers, rows = analyze_csv_file(file_path)
    except FileNotFoundError:
        sys.exit("文件名错误")
    profile = build_profile(headers, rows, preview)
    report = build_markdown_report(profile)

    print_profile(profile)
    if output_path:
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(report)
        print(f"报告已写入: {output_path}")
    if json_output_path:
        json_report = build_json_report(profile)
        with open(json_output_path, "w", encoding="utf-8") as file:
            file.write(json_report)
        print(f"JSON 报告已写入: {json_output_path}")


if __name__ == "__main__":
    main()
