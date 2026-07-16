from csv_profile import count_empty_values,count_duplicate_values


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
    result=count_duplicate_values(headers,rows)
    assert result == {
        "id": 0,
        "text": 2,
        "label": 2,
}
test_count_empty_values()
test_count_duplicate_values()
print("测试通过")