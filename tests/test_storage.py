"""
test_storage.py — Unit tests for modules/storage.py.

Uses pytest's tmp_path fixture so tests never touch the real data/ folder.
"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from modules.storage import (
    load_json,
    save_json,
    append_record,
    generate_id,
    get_timestamp,
    make_content_record,
    make_student_record,
)


# ---------------------------------------------------------------------------
# load_json
# ---------------------------------------------------------------------------

class TestLoadJson:
    def test_returns_empty_list_for_nonexistent_file(self, tmp_path):
        result = load_json(tmp_path / "does_not_exist.json")
        assert result == []

    def test_loads_valid_json_array(self, tmp_path):
        path = tmp_path / "data.json"
        path.write_text('[{"a": 1}, {"b": 2}]', encoding="utf-8")
        result = load_json(path)
        assert result == [{"a": 1}, {"b": 2}]

    def test_returns_empty_list_for_invalid_json(self, tmp_path):
        path = tmp_path / "bad.json"
        path.write_text("this is not json", encoding="utf-8")
        result = load_json(path)
        assert result == []

    def test_returns_empty_list_when_json_is_not_a_list(self, tmp_path):
        path = tmp_path / "dict.json"
        path.write_text('{"key": "value"}', encoding="utf-8")
        result = load_json(path)
        assert result == []

    def test_loads_empty_array(self, tmp_path):
        path = tmp_path / "empty.json"
        path.write_text("[]", encoding="utf-8")
        result = load_json(path)
        assert result == []


# ---------------------------------------------------------------------------
# save_json
# ---------------------------------------------------------------------------

class TestSaveJson:
    def test_saves_data_to_file(self, tmp_path):
        path = tmp_path / "output.json"
        records = [{"id": "abc", "value": 42}]
        success = save_json(path, records)
        assert success is True
        loaded = json.loads(path.read_text(encoding="utf-8"))
        assert loaded == records

    def test_creates_parent_directories(self, tmp_path):
        path = tmp_path / "sub" / "dir" / "data.json"
        success = save_json(path, [])
        assert success is True
        assert path.exists()

    def test_overwrites_existing_file(self, tmp_path):
        path = tmp_path / "data.json"
        save_json(path, [{"old": True}])
        save_json(path, [{"new": True}])
        loaded = json.loads(path.read_text(encoding="utf-8"))
        assert loaded == [{"new": True}]

    def test_saves_empty_list(self, tmp_path):
        path = tmp_path / "empty.json"
        success = save_json(path, [])
        assert success is True
        assert json.loads(path.read_text(encoding="utf-8")) == []


# ---------------------------------------------------------------------------
# append_record
# ---------------------------------------------------------------------------

class TestAppendRecord:
    def test_creates_file_on_first_call(self, tmp_path):
        path = tmp_path / "records.json"
        assert not path.exists()
        append_record(path, {"id": "1"})
        assert path.exists()

    def test_single_record_written(self, tmp_path):
        path = tmp_path / "records.json"
        append_record(path, {"id": "abc", "value": "hello"})
        data = json.loads(path.read_text(encoding="utf-8"))
        assert len(data) == 1
        assert data[0]["id"] == "abc"

    def test_accumulates_multiple_records(self, tmp_path):
        path = tmp_path / "records.json"
        append_record(path, {"id": "1"})
        append_record(path, {"id": "2"})
        append_record(path, {"id": "3"})
        data = json.loads(path.read_text(encoding="utf-8"))
        assert len(data) == 3

    def test_appends_to_existing_file(self, tmp_path):
        path = tmp_path / "records.json"
        save_json(path, [{"id": "existing"}])
        append_record(path, {"id": "new"})
        data = json.loads(path.read_text(encoding="utf-8"))
        assert len(data) == 2
        assert data[-1]["id"] == "new"


# ---------------------------------------------------------------------------
# generate_id
# ---------------------------------------------------------------------------

class TestGenerateId:
    def test_returns_non_empty_string(self):
        result = generate_id()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_returns_unique_values(self):
        ids = {generate_id() for _ in range(50)}
        assert len(ids) == 50


# ---------------------------------------------------------------------------
# get_timestamp
# ---------------------------------------------------------------------------

class TestGetTimestamp:
    def test_returns_string(self):
        result = get_timestamp()
        assert isinstance(result, str)

    def test_is_iso_format(self):
        import datetime
        result = get_timestamp()
        # Should parse without raising an exception
        dt = datetime.datetime.fromisoformat(result)
        assert dt is not None


# ---------------------------------------------------------------------------
# make_content_record
# ---------------------------------------------------------------------------

class TestMakeContentRecord:
    def test_record_has_required_keys(self):
        record = make_content_record(
            feature="lesson_plan",
            inputs={"topic": "Photosynthesis"},
            output="Here is your lesson plan...",
        )
        assert "id" in record
        assert "timestamp" in record
        assert "feature" in record
        assert "inputs" in record
        assert "output" in record

    def test_feature_stored_correctly(self):
        record = make_content_record("quiz", {}, "Questions here")
        assert record["feature"] == "quiz"

    def test_output_stored_correctly(self):
        record = make_content_record("activity", {}, "Activity text")
        assert record["output"] == "Activity text"


# ---------------------------------------------------------------------------
# make_student_record
# ---------------------------------------------------------------------------

class TestMakeStudentRecord:
    def test_record_has_required_keys(self):
        record = make_student_record(
            student_name="Alex",
            grade_level="Grade 7",
            subject="Mathematics",
            strengths="Good at algebra",
            weaknesses="Struggles with fractions",
            learning_style="Visual",
            recent_mark=72.5,
            ai_recommendation="Focus on fractions practice...",
        )
        for key in [
            "id", "timestamp", "student_name", "grade_level", "subject",
            "strengths", "weaknesses", "learning_style", "recent_mark",
            "ai_recommendation",
        ]:
            assert key in record

    def test_student_name_stored(self):
        record = make_student_record("Jordan", "Grade 9", "Science",
                                     "Creative", "Reading", "Auditory",
                                     None, "Recommendations...")
        assert record["student_name"] == "Jordan"

    def test_none_mark_stored_correctly(self):
        record = make_student_record("Pat", "Grade 5", "Art",
                                     "Creative", "Focus", "Visual",
                                     None, "Suggestions...")
        assert record["recent_mark"] is None
