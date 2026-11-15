
"""Helpers for teaching JSON Schema validation (not a solved lab)."""
from pathlib import Path
import yaml


def _convert_nullable(schema):
    """Convert OpenAPI 3.0 nullable into JSON Schema type unions."""
    if isinstance(schema, dict):
        converted = {
            key: _convert_nullable(value)
            for key, value in schema.items()
            if key != "nullable"
        }

        if schema.get("nullable") is True:
            schema_type = converted.get("type")

            if isinstance(schema_type, str):
                converted["type"] = [schema_type, "null"]
            elif isinstance(schema_type, list) and "null" not in schema_type:
                converted["type"] = schema_type + ["null"]

        return converted

    if isinstance(schema, list):
        return [_convert_nullable(item) for item in schema]

    return schema


def get_book_schema(path=None):
    spec_file = Path(path) if path else Path(__file__).parent / "openapi.yaml"
    spec = yaml.safe_load(spec_file.read_text(encoding="utf-8"))

    book_schema = spec["components"]["schemas"]["Book"]

    return _convert_nullable(book_schema)
