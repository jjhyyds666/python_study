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
    # 创建 ArgumentParser
    parser = argparse.ArgumentParser(description="检查CSV文件的数据质量")
    # 添加一个 file_path 参数
    parser.add_argument('file_path',help='要检查的CSV文件路径')

    parser.add_argument('--preview',type=int,default=5,help='预览前N行数据，默认5行')

    # 返回 parser.parse_args()
    return parser.parse_args()


def main():
    args=parse_args()
    file_path=args.file_path
    preview=args.preview
    try:
        headers, rows = analyze_csv_file(file_path)
    except FileNotFoundError:
        sys.exit("文件名错误")

    empty_counts = count_empty_values(headers, rows)
    duplicate_counts = count_duplicate_values(headers, rows)

    print(f"列名:{headers}")
    print(f"总数据行数:{len(rows)}")
    print(f"总列数:{len(headers)}")
    print(f"空值统计:{empty_counts}")
    print(f"每一列的重复值数量:{duplicate_counts}")
    print(f"前{preview}行:")

    for row in rows[:preview]:
        print(row)


if __name__ == "__main__":
    main()