import json

import pytest

from dataqa_cli.config_loader import load_config


def write_json_config(tmp_path, config_data):
    config_file = tmp_path / "rules.json"
    config_file.write_text(
        json.dumps(config_data),
        encoding="utf-8",
    )
    return config_file


def test_load_config(tmp_path):
    config_data = {
        "required_fields": ["id", "label"],
        "allowed_value_rules": {
            "label": ["positive", "negative"],
        },
    }
    config_file = write_json_config(tmp_path, config_data)

    result = load_config(config_file)

    assert result == config_data


def test_load_config_with_invalid_json(tmp_path):
    config_file = tmp_path / "rules.json"
    config_file.write_text(
        '{"required_fields": [',
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match=r"^配置文件不是有效的 JSON$",
    ):
        load_config(config_file)


def test_load_config_rejects_non_object(tmp_path):
    config_file = write_json_config(tmp_path, [])

    with pytest.raises(
        ValueError,
        match=r"^配置文件顶层必须是对象$",
    ):
        load_config(config_file)


def test_load_config_rejects_non_list_required_fields(tmp_path):
    config_file = write_json_config(
        tmp_path,
        {"required_fields": "id"},
    )

    with pytest.raises(
        ValueError,
        match=r"^required_fields 必须是字符串列表$",
    ):
        load_config(config_file)


def test_load_config_rejects_non_string_required_field(tmp_path):
    config_file = write_json_config(
        tmp_path,
        {"required_fields": ["id", 123]},
    )

    with pytest.raises(
        ValueError,
        match=r"^required_fields 必须是字符串列表$",
    ):
        load_config(config_file)


def test_load_config_rejects_non_object_allowed_value_rules(tmp_path):
    config_file = write_json_config(
        tmp_path,
        {"allowed_value_rules": []},
    )

    with pytest.raises(
        ValueError,
        match=(
            r"^allowed_value_rules 必须是字段到字符串列表的对象$"
        ),
    ):
        load_config(config_file)


def test_load_config_rejects_non_list_allowed_values(tmp_path):
    config_file = write_json_config(
        tmp_path,
        {"allowed_value_rules": {"label": "positive"}},
    )

    with pytest.raises(
        ValueError,
        match=(
            r"^allowed_value_rules 必须是字段到字符串列表的对象$"
        ),
    ):
        load_config(config_file)


def test_load_config_rejects_non_string_allowed_value(tmp_path):
    config_file = write_json_config(
        tmp_path,
        {"allowed_value_rules": {"label": ["positive", 123]}},
    )

    with pytest.raises(
        ValueError,
        match=(
            r"^allowed_value_rules 必须是字段到字符串列表的对象$"
        ),
    ):
        load_config(config_file)
