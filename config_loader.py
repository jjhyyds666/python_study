import json
from pathlib import Path
from typing import TypedDict


AllowedValueRules = dict[str, list[str]]


class Config(TypedDict):
    required_fields: list[str]
    allowed_value_rules: AllowedValueRules


def load_config(file_path: str | Path) -> Config:
    """读取并验证 JSON 配置文件。"""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            config_data: object = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError("配置文件不是有效的 JSON") from error

    return validate_config(config_data)


def validate_config(config_data: object) -> Config:
    """验证配置结构，并补齐可选规则的默认值。"""
    if not isinstance(config_data, dict):
        raise ValueError("配置文件顶层必须是对象")

    required_fields = config_data.get("required_fields", [])
    if not isinstance(required_fields, list):
        raise ValueError("required_fields 必须是字符串列表")

    clean_required_fields: list[str] = []
    for required_field in required_fields:
        if not isinstance(required_field, str):
            raise ValueError("required_fields 必须是字符串列表")
        clean_required_fields.append(required_field)

    allowed_value_rules = config_data.get("allowed_value_rules", {})
    if not isinstance(allowed_value_rules, dict):
        raise ValueError(
            "allowed_value_rules 必须是字段到字符串列表的对象"
        )

    clean_allowed_value_rules: AllowedValueRules = {}
    for field, allowed_values in allowed_value_rules.items():
        if not isinstance(field, str) or not isinstance(allowed_values, list):
            raise ValueError(
                "allowed_value_rules 必须是字段到字符串列表的对象"
            )

        clean_allowed_values: list[str] = []
        for allowed_value in allowed_values:
            if not isinstance(allowed_value, str):
                raise ValueError(
                    "allowed_value_rules 必须是字段到字符串列表的对象"
                )
            clean_allowed_values.append(allowed_value)

        clean_allowed_value_rules[field] = clean_allowed_values

    return {
        "required_fields": clean_required_fields,
        "allowed_value_rules": clean_allowed_value_rules,
    }
