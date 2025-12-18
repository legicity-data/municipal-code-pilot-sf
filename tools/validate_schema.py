import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

SCHEMA_PATH = Path("schemas/municipal_code_v1_1.schema.json")


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_schema.py <data.json>")
        sys.exit(0)

    data_path = Path(sys.argv[1])

    if not data_path.exists():
        print(f"❌ File not found: {data_path}")
        sys.exit(1)

    schema = load_json(SCHEMA_PATH)
    data = load_json(data_path)

    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)

    if not errors:
        print("✅ Schema validation passed")
        return

    print("⚠️ Schema validation warnings:")
    for error in errors:
        location = ".".join(str(p) for p in error.path)
        print(f"- {location}: {error.message}")


if __name__ == "__main__":
    main()
