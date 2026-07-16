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


if len(sys.argv) < 2:
    sys.exit("请输入 CSV 文件路径")

file_path = sys.argv[1]

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
print("前5行:")

for row in rows[:5]:
    print(row)