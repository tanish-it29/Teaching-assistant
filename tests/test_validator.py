"""
test_validator.py — Unit tests for modules/validator.py.

Tests cover: valid inputs, empty/missing inputs, boundary values, and
invalid type handling for all validator functions.
"""

import sys
import os

# Ensure the project root is on the path so `modules` can be imported
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from modules.validator import (
    validate_topic,
    validate_subject,
    validate_grade_level,
    validate_duration,
    validate_learning_objective,
    validate_difficulty,
    validate_question_type,
    validate_num_questions,
    validate_student_name,
    validate_student_text_field,
    validate_mark,
    validate_language,
    validate_content_to_translate,
    validate_learning_style,
    validate_credentials,
)


# ---------------------------------------------------------------------------
# validate_topic
# ---------------------------------------------------------------------------

class TestValidateTopic:
    def test_valid_topic(self):
        ok, msg = validate_topic("Photosynthesis")
        assert ok is True
        assert msg == ""

    def test_empty_topic(self):
        ok, msg = validate_topic("")
        assert ok is False
        assert msg != ""

    def test_whitespace_only_topic(self):
        ok, msg = validate_topic("   ")
        assert ok is False

    def test_too_short_topic(self):
        ok, msg = validate_topic("Ab")
        assert ok is False

    def test_minimum_length_topic(self):
        ok, msg = validate_topic("ABC")
        assert ok is True

    def test_maximum_length_topic(self):
        ok, msg = validate_topic("A" * 300)
        assert ok is True

    def test_too_long_topic(self):
        ok, msg = validate_topic("A" * 301)
        assert ok is False

    def test_none_topic(self):
        ok, msg = validate_topic(None)  # type: ignore[arg-type]
        assert ok is False


# ---------------------------------------------------------------------------
# validate_subject
# ---------------------------------------------------------------------------

class TestValidateSubject:
    def test_valid_subject(self):
        ok, msg = validate_subject("Mathematics")
        assert ok is True
        assert msg == ""

    def test_empty_subject(self):
        ok, msg = validate_subject("")
        assert ok is False

    def test_too_long_subject(self):
        ok, msg = validate_subject("A" * 101)
        assert ok is False

    def test_max_length_subject(self):
        ok, msg = validate_subject("A" * 100)
        assert ok is True


# ---------------------------------------------------------------------------
# validate_grade_level
# ---------------------------------------------------------------------------

class TestValidateGradeLevel:
    def test_valid_grade(self):
        ok, msg = validate_grade_level("Grade 5")
        assert ok is True

    def test_invalid_grade(self):
        ok, msg = validate_grade_level("Grade 99")
        assert ok is False

    def test_empty_grade(self):
        ok, msg = validate_grade_level("")
        assert ok is False

    def test_university_level(self):
        ok, msg = validate_grade_level("University / College")
        assert ok is True


# ---------------------------------------------------------------------------
# validate_duration
# ---------------------------------------------------------------------------

class TestValidateDuration:
    def test_valid_duration(self):
        ok, msg = validate_duration(45)
        assert ok is True

    def test_minimum_duration(self):
        ok, msg = validate_duration(10)
        assert ok is True

    def test_below_minimum_duration(self):
        ok, msg = validate_duration(9)
        assert ok is False

    def test_maximum_duration(self):
        ok, msg = validate_duration(300)
        assert ok is True

    def test_above_maximum_duration(self):
        ok, msg = validate_duration(301)
        assert ok is False

    def test_non_numeric_duration(self):
        ok, msg = validate_duration("forty-five")  # type: ignore[arg-type]
        assert ok is False

    def test_none_duration(self):
        ok, msg = validate_duration(None)  # type: ignore[arg-type]
        assert ok is False


# ---------------------------------------------------------------------------
# validate_learning_objective
# ---------------------------------------------------------------------------

class TestValidateLearningObjective:
    def test_valid_objective(self):
        ok, msg = validate_learning_objective("Students will understand photosynthesis.")
        assert ok is True

    def test_empty_objective(self):
        ok, msg = validate_learning_objective("")
        assert ok is False

    def test_too_long_objective(self):
        ok, msg = validate_learning_objective("A" * 501)
        assert ok is False

    def test_max_length_objective(self):
        ok, msg = validate_learning_objective("A" * 500)
        assert ok is True


# ---------------------------------------------------------------------------
# validate_num_questions
# ---------------------------------------------------------------------------

class TestValidateNumQuestions:
    def test_valid_number(self):
        ok, msg = validate_num_questions(5)
        assert ok is True

    def test_minimum(self):
        ok, msg = validate_num_questions(1)
        assert ok is True

    def test_below_minimum(self):
        ok, msg = validate_num_questions(0)
        assert ok is False

    def test_maximum(self):
        ok, msg = validate_num_questions(20)
        assert ok is True

    def test_above_maximum(self):
        ok, msg = validate_num_questions(21)
        assert ok is False

    def test_non_numeric(self):
        ok, msg = validate_num_questions("five")  # type: ignore[arg-type]
        assert ok is False

    def test_none_value(self):
        ok, msg = validate_num_questions(None)  # type: ignore[arg-type]
        assert ok is False


# ---------------------------------------------------------------------------
# validate_mark
# ---------------------------------------------------------------------------

class TestValidateMark:
    def test_valid_mark(self):
        ok, msg = validate_mark(75.0)
        assert ok is True

    def test_zero_mark(self):
        ok, msg = validate_mark(0.0)
        assert ok is True

    def test_hundred_mark(self):
        ok, msg = validate_mark(100.0)
        assert ok is True

    def test_below_zero(self):
        ok, msg = validate_mark(-1.0)
        assert ok is False

    def test_above_hundred(self):
        ok, msg = validate_mark(101.0)
        assert ok is False

    def test_non_numeric_mark(self):
        ok, msg = validate_mark("excellent")  # type: ignore[arg-type]
        assert ok is False

    def test_none_mark(self):
        ok, msg = validate_mark(None)  # type: ignore[arg-type]
        assert ok is False


# ---------------------------------------------------------------------------
# validate_language
# ---------------------------------------------------------------------------

class TestValidateLanguage:
    def test_valid_language(self):
        ok, msg = validate_language("French")
        assert ok is True

    def test_invalid_language(self):
        ok, msg = validate_language("Klingon")
        assert ok is False

    def test_empty_language(self):
        ok, msg = validate_language("")
        assert ok is False

    def test_english(self):
        ok, msg = validate_language("English")
        assert ok is True


# ---------------------------------------------------------------------------
# validate_content_to_translate
# ---------------------------------------------------------------------------

class TestValidateContentToTranslate:
    def test_valid_content(self):
        ok, msg = validate_content_to_translate("Plants need sunlight to grow.")
        assert ok is True

    def test_empty_content(self):
        ok, msg = validate_content_to_translate("")
        assert ok is False

    def test_too_long_content(self):
        ok, msg = validate_content_to_translate("A" * 2001)
        assert ok is False

    def test_max_length_content(self):
        ok, msg = validate_content_to_translate("A" * 2000)
        assert ok is True


# ---------------------------------------------------------------------------
# validate_credentials
# ---------------------------------------------------------------------------

class TestValidateCredentials:
    def test_valid_credentials(self):
        ok, msg = validate_credentials("api-key-123", "proj-id-456", "https://us-south.ml.cloud.ibm.com")
        assert ok is True

    def test_missing_api_key(self):
        ok, msg = validate_credentials("", "proj-id-456", "https://us-south.ml.cloud.ibm.com")
        assert ok is False

    def test_missing_project_id(self):
        ok, msg = validate_credentials("api-key-123", "", "https://us-south.ml.cloud.ibm.com")
        assert ok is False

    def test_missing_url(self):
        ok, msg = validate_credentials("api-key-123", "proj-id-456", "")
        assert ok is False

    def test_whitespace_only_key(self):
        ok, msg = validate_credentials("   ", "proj-id-456", "https://us-south.ml.cloud.ibm.com")
        assert ok is False


# ---------------------------------------------------------------------------
# validate_student_text_field
# ---------------------------------------------------------------------------

class TestValidateStudentTextField:
    def test_valid_field(self):
        ok, msg = validate_student_text_field("Good at algebra", "Strengths")
        assert ok is True

    def test_empty_field(self):
        ok, msg = validate_student_text_field("", "Strengths")
        assert ok is False
        assert "Strengths" in msg

    def test_too_long_field(self):
        ok, msg = validate_student_text_field("A" * 501, "Weaknesses")
        assert ok is False


# ---------------------------------------------------------------------------
# validate_learning_style
# ---------------------------------------------------------------------------

class TestValidateLearningStyle:
    def test_valid_style(self):
        ok, msg = validate_learning_style("Visual")
        assert ok is True

    def test_invalid_style(self):
        ok, msg = validate_learning_style("Unknown style")
        assert ok is False

    def test_empty_style(self):
        ok, msg = validate_learning_style("")
        assert ok is False


# ---------------------------------------------------------------------------
# validate_difficulty
# ---------------------------------------------------------------------------

class TestValidateDifficulty:
    def test_valid_difficulty(self):
        ok, msg = validate_difficulty("Medium")
        assert ok is True

    def test_invalid_difficulty(self):
        ok, msg = validate_difficulty("Extreme")
        assert ok is False

    def test_empty_difficulty(self):
        ok, msg = validate_difficulty("")
        assert ok is False
