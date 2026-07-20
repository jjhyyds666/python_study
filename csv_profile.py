import argparse
import csv
import sys


def analyze_csv_file(file_path):
    with open(file_path, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames
        rows = list(reader)

    return headers, rows


def count_empty_values(headers, rows):
    empty_counts = {}

    for header in headers:
        empty_counts[header] = 0

    for row in rows:
        for header in headers:
            if row[header].strip() == "":
                empty_counts[header] += 1

    return empty_counts


def count_duplicate_values(headers, rows):
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
    parser = argparse.ArgumentParser(description="检查 CSV 文件的数据质量")
    parser.add_argument("file_path", help="要检查的 CSV 文件路径")
    parser.add_argument(
        "--preview",
        type=int,
        default=5,
        help="预览前 N 行数据，默认 5 行",
    )
    parser.add_argument("--output", help="将 Markdown 报告写入指定文件")

    args = parser.parse_args()

    if args.preview < 0:
        parser.error("--preview 不能是负数")

    return args


def count_unique_values(headers, rows):
    unique_counts = {}

    for header in headers:
        unique_values = {}

        for row in rows:
            value = row[header].strip()
            unique_values[value] = 1

        unique_counts[header] = len(unique_values)

    return unique_counts


def build_markdown_report(profile):
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
    return {
        "headers": headers,
        "row_count": len(rows),
        "column_count": len(headers),
        "preview": rows[:preview],
        "empty_counts": count_empty_values(headers, rows),
        "duplicate_counts": count_duplicate_values(headers, rows),
        "unique_counts": count_unique_values(headers, rows),
    }


def main():
    args = parse_args()
    file_path = args.file_path
    preview = args.preview
    output_path = args.output

    try:
        headers, rows = analyze_csv_file(file_path)
    except FileNotFoundError:
        sys.exit("文件名错误")

    profile = build_profile(headers, rows, preview)
    print(f"列名:{profile['headers']}")
    print(f"总数据行数:{profile['row_count']}")
    print(f"总列数:{profile['column_count']}")
    print(f"空值统计:{profile['empty_counts']}")
    print(f"每一列的重复值数量:{profile['duplicate_counts']}")
    print(f"每一列唯一值：{profile['unique_counts']}")
    for row in profile["preview"]:
        print(row)

    report = build_markdown_report(profile)

    if output_path:
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(report)
        print(f"报告已写入: {output_path}")


if __name__ == "__main__":
    main()
