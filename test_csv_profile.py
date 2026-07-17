from csv_profile import analyze_csv_file, count_empty_values, count_duplicate_values


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
