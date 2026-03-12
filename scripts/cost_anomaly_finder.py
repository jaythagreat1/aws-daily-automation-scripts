import csv
import json
import os
from datetime import datetime, timezone


def ensure_output_dir() -> None:
    os.makedirs("output", exist_ok=True)


def timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")


def write_csv(filename: str, fieldnames: list[str], rows: list[dict]) -> None:
    ensure_output_dir()
    filepath = os.path.join("output", filename)

    with open(filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        if rows:
            writer.writerows(rows)

    print(f"Saved CSV: {filepath}")


def write_json(filename: str, data: dict | list) -> None:
    ensure_output_dir()
    filepath = os.path.join("output", filename)

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, default=str)

    print(f"Saved JSON: {filepath}")


def safe_get_tags(tags: list[dict] | None) -> dict[str, str]:
    if not tags:
        return {}
    return {
        tag.get("Key", ""): tag.get("Value", "")
        for tag in tags
        if tag.get("Key")
    }