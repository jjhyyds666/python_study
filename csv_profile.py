import argparse
import csv
import json
import sys


# 数据读取与基础统计


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


def count_unique_values(headers, rows):
    """统计每一列去重后的唯一值数量。"""
    unique_counts = {}

    for header in headers:
        values = set()

        for row in rows:
            values.add(row[header].strip())

        unique_counts[header] = len(values)

    return unique_counts


# 字段规则校验


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


def validate_allowed_values(headers, rows, field, allowed_values):
    """检查指定字段中非空值是否属于允许值列表。"""
    return_allowed_values = {
        "field": field,
        "missing_field": True,
        "invalid_count": 0,
        "invalid_values": [],
    }
    clean_allowed_values = {
        allowed_value.strip() for allowed_value in allowed_values
    }

    if field not in headers:
        return return_allowed_values

    return_allowed_values["missing_field"] = False

    for row in rows:
        value = row[field].strip()

        if value == "":
            continue

        if value in clean_allowed_values:
            continue

        return_allowed_values["invalid_count"] += 1

        if value not in return_allowed_values["invalid_values"]:
            return_allowed_values["invalid_values"].append(value)

    return return_allowed_values


# 数据画像汇总与报告输出


def build_profile(
    headers,
    rows,
    preview,
    required_fields=None,
    allowed_value_rules=None,
):
    """汇总 CSV 的基础信息、字段统计、规则校验和预览数据。"""
    if required_fields is None:
        required_fields = []

    if allowed_value_rules is None:
        allowed_value_rules = {}

    allowed_value_validations = {}

    for field, allowed_values in allowed_value_rules.items():
        allowed_value_validations[field] = validate_allowed_values(
            headers,
            rows,
            field,
            allowed_values,
        )

    return {
        "headers": headers,
        "row_count": len(rows),
        "column_count": len(headers),
        "preview": rows[:preview],
        "empty_counts": count_empty_values(headers, rows),
        "duplicate_counts": count_duplicate_values(headers, rows),
        "unique_counts": count_unique_values(headers, rows),
        "required_validation": validate_required_fields(headers, rows, required_fields),
        "allowed_value_validations": allowed_value_validations,
    }


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

    required_validation = profile.get("required_validation", {})
    missing_fields = required_validation.get("missing_fields", [])
    empty_required_counts = required_validation.get("empty_required_counts", {})

    if missing_fields or empty_required_counts:
        lines.append("")
        lines.append("## 必填字段检查")
        lines.append("")
        lines.append(
            f"- 缺失的必填字段: {', '.join(missing_fields) if missing_fields else '无'}"
        )
        lines.append("")
        lines.append("| 必填字段 | 空值数量 |")
        lines.append("| --- | ---: |")

        for field, empty_count in empty_required_counts.items():
            lines.append(f"| {field} | {empty_count} |")

    allowed_value_validations = profile.get("allowed_value_validations", {})

    if allowed_value_validations:
        lines.append("")
        lines.append("## 合法值检查")
        lines.append("")
        lines.append("| 字段 | 字段缺失 | 非法值数量 | 非法值 |")
        lines.append("| --- | --- | ---: | --- |")

        for field, validation in allowed_value_validations.items():
            missing_field = "是" if validation["missing_field"] else "否"
            invalid_values = ", ".join(validation["invalid_values"]) or "无"
            lines.append(
                f"| {field} | {missing_field} | "
                f"{validation['invalid_count']} | {invalid_values} |"
            )

    lines.append("")
    lines.append(f"## 前 {len(profile['preview'])} 行预览")
    lines.append("")

    for row in profile["preview"]:
        lines.append(f"- {row}")

    return "\n".join(lines)


def build_json_report(profile):
    """根据数据画像 profile 生成格式化后的 JSON 字符串。"""
    return json.dumps(profile, ensure_ascii=False, indent=2)


def print_profile(profile):
    """将数据画像的主要统计结果打印到命令行。"""
    print(f"列名:{profile['headers']}")
    print(f"总数据行数:{profile['row_count']}")
    print(f"总列数:{profile['column_count']}")
    print(f"空值统计:{profile['empty_counts']}")
    print(f"每一列的重复值数量:{profile['duplicate_counts']}")
    print(f"每一列唯一值：{profile['unique_counts']}")

    required_validation = profile["required_validation"]
    print(f"缺失的必填字段:{required_validation['missing_fields']}")
    print(f"必填字段空值统计:{required_validation['empty_required_counts']}")

    for field, validation in profile["allowed_value_validations"].items():
        print(f"{field} 字段是否缺失:{validation['missing_field']}")
        print(f"{field} 非法值数量:{validation['invalid_count']}")
        print(f"{field} 非法值:{validation['invalid_values']}")

    for row in profile["preview"]:
        print(row)


# 命令行入口


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
    parser.add_argument(
        "--required",
        nargs="*",
        default=[],
        help="需要检查为必填的字段，例如 --required label text",
    )
    parser.add_argument(
        "--allowed-labels",
        nargs="+",
        help="label 字段允许的值，例如 --allowed-labels positive negative",
    )
    args = parser.parse_args()

    if args.preview < 0:
        parser.error("--preview 不能是负数")

    return args


def main():
    """程序入口：读取参数、分析 CSV，并按需输出 Markdown 或 JSON 报告。"""
    args = parse_args()
    allowed_value_rules = {}

    if args.allowed_labels is not None:
        allowed_value_rules["label"] = args.allowed_labels

    try:
        headers, rows = analyze_csv_file(args.file_path)
    except FileNotFoundError:
        sys.exit("文件名错误")

    profile = build_profile(
        headers,
        rows,
        args.preview,
        required_fields=args.required,
        allowed_value_rules=allowed_value_rules,
    )
    report = build_markdown_report(profile)

    print_profile(profile)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as file:
            file.write(report)
        print(f"报告已写入: {args.output}")

    if args.json_output:
        json_report = build_json_report(profile)
        with open(args.json_output, "w", encoding="utf-8") as file:
            file.write(json_report)
        print(f"JSON 报告已写入: {args.json_output}")


if __name__ == "__main__":
    main()
