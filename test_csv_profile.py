from csv_profile import (
    analyze_csv_file,
    build_markdown_report,
    count_duplicate_values,
    count_empty_values,
    count_unique_values,
)


def test_count_empty_values():
    headers = ["id", "text", "label"]

    rows = [
        {"id": "1", "text": "hello", "label": "positive"},
        {"id": "2", "text": "", "label": "negative"},
        {"id": "3", "text": "world", "label": ""},
    ]

    result = count_empty_values(headers, rows)

    assert result == {
        "id": 0,
        "text": 1,
        "label": 1,
    }


def test_count_duplicate_values():
    headers = ["id", "text", "label"]

    rows = [
        {"id": "1", "text": "hello", "label": "positive"},
        {"id": "2", "text": "hello", "label": "positive"},
        {"id": "3", "text": "world", "label": "negative"},
        {"id": "4", "text": "hello", "label": "negative"},
    ]

    result = count_duplicate_values(headers, rows)

    assert result == {
        "id": 0,
        "text": 2,
        "label": 2,
    }


def test_count_empty_values_with_spaces():
    headers = ["id", "text", "label"]

    rows = [
        {"id": "1", "text": "   ", "label": "positive"},
        {"id": "2", "text": "hello", "label": "   "},
    ]

    result = count_empty_values(headers, rows)

    assert result == {
        "id": 0,
        "text": 1,
        "label": 1,
    }


def test_analyze_csv_file(tmp_path):
    csv_file = tmp_path / "test.csv"

    csv_file.write_text(
        "id,text,label\n"
        "1,hello,positive\n"
        "2,world,negative\n",
        encoding="utf-8",
    )

    headers, rows = analyze_csv_file(csv_file)

    assert headers == ["id", "text", "label"]
    assert len(rows) == 2
    assert rows[0] == {"id": "1", "text": "hello", "label": "positive"}
    assert rows[1] == {"id": "2", "text": "world", "label": "negative"}


def test_count_unique_values():
    headers = ["id", "label"]

    rows = [
        {"id": "1", "label": "1"},
        {"id": "2", "label": "2"},
        {"id": "2", "label": "1"},
    ]

    result = count_unique_values(headers, rows)

    assert result == {
        "id": 2,
        "label": 2,
    }


def test_build_markdown_report():
    headers = ["id", "label"]

    rows = [
        {"id": "1", "label": "positive"},
        {"id": "2", "label": ""},
    ]

    empty_counts = {"id": 0, "label": 1}
    duplicate_counts = {"id": 0, "label": 0}
    unique_counts = {"id": 2, "label": 2}
    preview = 1

    report = build_markdown_report(
        headers,
        rows,
        empty_counts,
        duplicate_counts,
        unique_counts,
        preview,
    )

    assert "# CSV 数据质量报告" in report
    assert "总数据行数" in report
    assert "空值统计" in report
    assert "重复值统计" in report
    assert "唯一值统计" in report
    assert "positive" in report
