from csv_profile import (
    analyze_csv_file,
    build_json_report,
    build_profile,
    build_markdown_report,
    count_duplicate_values,
    count_empty_values,
    count_unique_values,
    validate_required_fields,
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

    profile = {
        "headers": headers,
        "row_count": len(rows),
        "column_count": len(headers),
        "preview": rows[:preview],
        "empty_counts": empty_counts,
        "duplicate_counts": duplicate_counts,
        "unique_counts": unique_counts,
    }

    report = build_markdown_report(profile)

    assert "# CSV 数据质量报告" in report
    assert "总数据行数" in report
    assert "## 字段统计" in report
    assert "| 字段 | 空值数量 | 重复值数量 | 唯一值数量 |" in report
    assert "| label | 1 | 0 | 2 |" in report
    assert "## 前 1 行预览" in report
    assert "positive" in report


def test_build_profile():
    headers = ["id", "label"]

    rows = [
        {"id": "1", "label": "positive"},
        {"id": "2", "label": ""},
        {"id": "2", "label": "positive"},
    ]

    profile = build_profile(headers, rows, 2)
    assert profile["preview"] == rows[:2]
    assert profile["headers"] == headers
    assert profile["row_count"] == 3
    assert profile["column_count"] == 2
    assert profile["empty_counts"] == {"id": 0, "label": 1}
    assert profile["duplicate_counts"] == {"id": 1, "label": 1}
    assert profile["unique_counts"] == {"id": 2, "label": 2}


def test_count_unique_values_strips_spaces():
    headers = ["label"]

    rows = [
        {"label": "positive"},
        {"label": " positive "},
        {"label": "positive   "},
        {"label": "negative"},
    ]

    result = count_unique_values(headers, rows)

    assert result == {
        "label": 2,
    }


def test_build_json_report():
    profile = {
        "headers": ["id", "label"],
        "row_count": 2,
        "column_count": 2,
        "preview": [
            {"id": "1", "label": "positive"},
        ],
        "empty_counts": {"id": 0, "label": 1},
        "duplicate_counts": {"id": 0, "label": 0},
        "unique_counts": {"id": 2, "label": 2},
    }

    report = build_json_report(profile)

    assert '"row_count": 2' in report
    assert '"label": 1' in report
    assert "positive" in report


def test_validate_required_fields():
    headers = ["id", "text", "label"]

    rows = [
        {"id": "1", "text": "hello", "label": "positive"},
        {"id": "2", "text": "", "label": ""},
    ]

    required_fields = ["text", "label"]

    report = validate_required_fields(headers, rows, required_fields)

    assert report == {
        "missing_fields": [],
        "empty_required_counts": {
            "text": 1,
            "label": 1,
        },
    }


def test_validate_required_fields_with_missing_field():
    headers = ["id", "text", "label"]

    rows = [
        {"id": "1", "text": "hello", "label": "positive"},
        {"id": "2", "text": "world", "label": "negative"},
    ]

    required_fields = ["label", "annotator"]

    report = validate_required_fields(headers, rows, required_fields)

    assert report == {
        "missing_fields": ["annotator"],
        "empty_required_counts": {
            "label": 0,
        },
    }
