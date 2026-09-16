"""
test_prompt_builder.py — Unit tests for modules/prompt_builder.py.

For each builder function we verify:
  - The return value is a non-empty string
  - Key input values appear in the returned string
  - The output contains the expected role instruction phrase
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from modules.prompt_builder import (
    build_lesson_plan_prompt,
    build_quiz_prompt,
    build_assessment_prompt,
    build_recommendation_prompt,
    build_multilingual_prompt,
    build_activity_prompt,
    build_resource_prompt,
)


# ---------------------------------------------------------------------------
# build_lesson_plan_prompt
# ---------------------------------------------------------------------------

class TestBuildLessonPlanPrompt:
    def _make(self, **kwargs):
        defaults = dict(
            subject="Biology",
            topic="Photosynthesis",
            grade_level="Grade 9",
            duration_minutes=60,
            learning_objective="Understand how plants make food",
        )
        defaults.update(kwargs)
        return build_lesson_plan_prompt(**defaults)

    def test_returns_non_empty_string(self):
        assert isinstance(self._make(), str)
        assert len(self._make()) > 0

    def test_contains_subject(self):
        assert "Biology" in self._make()

    def test_contains_topic(self):
        assert "Photosynthesis" in self._make()

    def test_contains_grade(self):
        assert "Grade 9" in self._make()

    def test_contains_duration(self):
        assert "60" in self._make()

    def test_contains_objective(self):
        assert "plants make food" in self._make()

    def test_contains_role_instruction(self):
        result = self._make()
        assert "teacher" in result.lower()

    def test_contains_section_headings(self):
        result = self._make()
        assert "Learning Objectives" in result
        assert "Assessment" in result


# ---------------------------------------------------------------------------
# build_quiz_prompt — MCQ
# ---------------------------------------------------------------------------

class TestBuildQuizPromptMCQ:
    def _make(self, **kwargs):
        defaults = dict(
            topic="Fractions",
            grade_level="Grade 6",
            difficulty="Medium",
            num_questions=5,
            question_type="Multiple Choice (MCQ)",
        )
        defaults.update(kwargs)
        return build_quiz_prompt(**defaults)

    def test_returns_non_empty_string(self):
        assert isinstance(self._make(), str)
        assert len(self._make()) > 0

    def test_contains_topic(self):
        assert "Fractions" in self._make()

    def test_contains_difficulty(self):
        assert "Medium" in self._make()

    def test_contains_question_count(self):
        assert "5" in self._make()

    def test_contains_mcq_instruction(self):
        result = self._make()
        assert "A, B, C, D" in result or "multiple-choice" in result.lower()


# ---------------------------------------------------------------------------
# build_quiz_prompt — Short Answer
# ---------------------------------------------------------------------------

class TestBuildQuizPromptShortAnswer:
    def test_contains_short_answer_instruction(self):
        result = build_quiz_prompt(
            topic="World War II",
            grade_level="Grade 10",
            difficulty="Hard",
            num_questions=4,
            question_type="Short Answer",
        )
        assert "short-answer" in result.lower() or "short answer" in result.lower()


# ---------------------------------------------------------------------------
# build_quiz_prompt — Mixed
# ---------------------------------------------------------------------------

class TestBuildQuizPromptMixed:
    def test_contains_mixed_instruction(self):
        result = build_quiz_prompt(
            topic="Newton's Laws",
            grade_level="Grade 11",
            difficulty="Easy",
            num_questions=6,
            question_type="Mixed (MCQ + Short Answer)",
        )
        assert "multiple-choice" in result.lower() or "short-answer" in result.lower()


# ---------------------------------------------------------------------------
# build_assessment_prompt
# ---------------------------------------------------------------------------

class TestBuildAssessmentPrompt:
    def _make(self, **kwargs):
        defaults = dict(
            topic="Algebra",
            grade_level="Grade 8",
            difficulty="Hard",
            num_questions=10,
        )
        defaults.update(kwargs)
        return build_assessment_prompt(**defaults)

    def test_returns_non_empty_string(self):
        assert isinstance(self._make(), str)
        assert len(self._make()) > 0

    def test_contains_topic(self):
        assert "Algebra" in self._make()

    def test_contains_model_answer_instruction(self):
        assert "model answer" in self._make().lower() or "Model Answer" in self._make()

    def test_contains_question_count(self):
        assert "10" in self._make()

    def test_contains_grade_level(self):
        assert "Grade 8" in self._make()


# ---------------------------------------------------------------------------
# build_recommendation_prompt
# ---------------------------------------------------------------------------

class TestBuildRecommendationPrompt:
    def _make(self, **kwargs):
        defaults = dict(
            student_name="Alex",
            grade_level="Grade 7",
            subject="Mathematics",
            strengths="Good at algebra and problem solving",
            weaknesses="Struggles with fractions and word problems",
            learning_style="Visual",
            recent_mark=65.0,
        )
        defaults.update(kwargs)
        return build_recommendation_prompt(**defaults)

    def test_returns_non_empty_string(self):
        assert isinstance(self._make(), str)
        assert len(self._make()) > 0

    def test_contains_student_name(self):
        assert "Alex" in self._make()

    def test_contains_subject(self):
        assert "Mathematics" in self._make()

    def test_contains_learning_style(self):
        assert "Visual" in self._make()

    def test_contains_strengths(self):
        assert "algebra" in self._make()

    def test_contains_weaknesses(self):
        assert "fractions" in self._make()

    def test_contains_mark_when_provided(self):
        assert "65" in self._make()

    def test_no_mark_when_none(self):
        result = self._make(recent_mark=None)
        assert "%" not in result or "65" not in result

    def test_contains_disclaimer(self):
        result = self._make()
        assert "teacher" in result.lower()

    def test_anonymous_student(self):
        result = self._make(student_name="")
        assert "the student" in result


# ---------------------------------------------------------------------------
# build_multilingual_prompt
# ---------------------------------------------------------------------------

class TestBuildMultilingualPrompt:
    def _make(self, **kwargs):
        defaults = dict(
            content="The water cycle describes how water moves through the environment.",
            target_language="French",
        )
        defaults.update(kwargs)
        return build_multilingual_prompt(**defaults)

    def test_returns_non_empty_string(self):
        assert isinstance(self._make(), str)
        assert len(self._make()) > 0

    def test_contains_target_language(self):
        assert "French" in self._make()

    def test_contains_original_content(self):
        assert "water cycle" in self._make()

    def test_role_instruction_present(self):
        assert "translator" in self._make().lower() or "translat" in self._make().lower()


# ---------------------------------------------------------------------------
# build_activity_prompt
# ---------------------------------------------------------------------------

class TestBuildActivityPrompt:
    def _make(self, **kwargs):
        defaults = dict(
            topic="Ecosystems",
            grade_level="Grade 6",
            subject="Science",
        )
        defaults.update(kwargs)
        return build_activity_prompt(**defaults)

    def test_returns_non_empty_string(self):
        assert isinstance(self._make(), str)
        assert len(self._make()) > 0

    def test_contains_topic(self):
        assert "Ecosystems" in self._make()

    def test_contains_grade_level(self):
        assert "Grade 6" in self._make()

    def test_contains_materials_instruction(self):
        assert "materials" in self._make().lower()

    def test_contains_subject(self):
        assert "Science" in self._make()

    def test_works_without_subject(self):
        result = build_activity_prompt(topic="Shapes", grade_level="Grade 3")
        assert "Shapes" in result


# ---------------------------------------------------------------------------
# build_resource_prompt
# ---------------------------------------------------------------------------

class TestBuildResourcePrompt:
    def _make(self, **kwargs):
        defaults = dict(
            topic="Forces and Motion",
            grade_level="Grade 10",
            subject="Physics",
        )
        defaults.update(kwargs)
        return build_resource_prompt(**defaults)

    def test_returns_non_empty_string(self):
        assert isinstance(self._make(), str)
        assert len(self._make()) > 0

    def test_contains_topic(self):
        assert "Forces and Motion" in self._make()

    def test_contains_grade_level(self):
        assert "Grade 10" in self._make()

    def test_contains_key_sections(self):
        result = self._make()
        assert "Key Concepts" in result
        assert "Practice Questions" in result
        assert "Discussion" in result

    def test_works_without_subject(self):
        result = build_resource_prompt(topic="Climate Change", grade_level="Grade 9")
        assert "Climate Change" in result
