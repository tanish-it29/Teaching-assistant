"""
storage.py — Simple JSON persistence helpers.

Handles reading and writing records to local JSON files.
All errors are caught and logged to stderr — they never crash the UI.
"""

import json
import uuid
import datetime
import sys
from pathlib import Path
from typing import Any


def load_json(filepath: Path | str) -> list[dict[str, Any]]:
    """
    Load a JSON array from a file.
    Returns an empty list if the file does not exist or cannot be parsed.
    """
    path = Path(filepath)
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as exc:
        print(f"[storage] Warning: could not parse {path}: {exc}", file=sys.stderr)
        return []
    except OSError as exc:
        print(f"[storage] Warning: could not read {path}: {exc}", file=sys.stderr)
        return []


def save_json(filepath: Path | str, data: list[dict[str, Any]]) -> bool:
    """
    Write a list of dicts to a JSON file, overwriting any existing content.
    Returns True on success, False on failure.
    """
    path = Path(filepath)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except OSError as exc:
        print(f"[storage] Warning: could not write {path}: {exc}", file=sys.stderr)
        return False


def append_record(filepath: Path | str, record: dict[str, Any]) -> bool:
    """
    Append a single record dict to the JSON array in a file.
    Creates the file if it does not exist.
    Returns True on success, False on failure.
    """
    records = load_json(filepath)
    records.append(record)
    return save_json(filepath, records)


def generate_id() -> str:
    """Return a short random ID string (first 8 characters of a UUID4)."""
    return str(uuid.uuid4())[:8]


def get_timestamp() -> str:
    """Return the current local datetime as an ISO 8601 string."""
    return datetime.datetime.now().isoformat()


def make_content_record(
    feature: str,
    inputs: dict[str, Any],
    output: str,
) -> dict[str, Any]:
    """
    Build a GeneratedContentRecord dict ready to be saved.

    Args:
        feature: one of 'lesson_plan', 'quiz', 'assessment',
                 'recommendation', 'multilingual', 'activity', 'resource'
        inputs:  the form fields the teacher submitted (as a plain dict)
        output:  the full AI-generated text
    """
    return {
        "id": generate_id(),
        "timestamp": get_timestamp(),
        "feature": feature,
        "inputs": inputs,
        "output": output,
    }


def make_student_record(
    student_name: str,
    grade_level: str,
    subject: str,
    strengths: str,
    weaknesses: str,
    learning_style: str,
    recent_mark: float | None,
    ai_recommendation: str,
) -> dict[str, Any]:
    """Build a StudentRecord dict ready to be saved."""
    return {
        "id": generate_id(),
        "timestamp": get_timestamp(),
        "student_name": student_name,
        "grade_level": grade_level,
        "subject": subject,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "learning_style": learning_style,
        "recent_mark": recent_mark,
        "ai_recommendation": ai_recommendation,
    }
