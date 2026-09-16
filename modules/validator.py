"""
validator.py — Input validation functions.

Every function returns a tuple (is_valid: bool, error_message: str).
When valid, error_message is an empty string.
No side effects — pure functions, easy to unit-test.
"""

from modules.config import (
    GRADE_LEVELS,
    SUPPORTED_LANGUAGES,
    DIFFICULTY_LEVELS,
    QUESTION_TYPES,
    LEARNING_STYLES,
    MIN_QUESTIONS,
    MAX_QUESTIONS,
    MIN_MARK,
    MAX_MARK,
)


def validate_topic(topic: str) -> tuple[bool, str]:
    """Topic must be a non-empty string between 3 and 300 characters."""
    stripped = topic.strip() if topic else ""
    if not stripped:
        return False, "Topic is required."
    if len(stripped) < 3:
        return False, "Topic must be at least 3 characters."
    if len(stripped) > 300:
        return False, "Topic must be 300 characters or fewer."
    return True, ""


def validate_subject(subject: str) -> tuple[bool, str]:
    """Subject must be a non-empty string of up to 100 characters."""
    stripped = subject.strip() if subject else ""
    if not stripped:
        return False, "Subject is required."
    if len(stripped) > 100:
        return False, "Subject must be 100 characters or fewer."
    return True, ""


def validate_grade_level(grade_level: str) -> tuple[bool, str]:
    """Grade level must be chosen from the predefined list."""
    if not grade_level or grade_level.strip() not in GRADE_LEVELS:
        return False, f"Please select a valid grade level."
    return True, ""


def validate_duration(duration: int | float) -> tuple[bool, str]:
    """Duration in minutes must be between 10 and 300."""
    try:
        val = int(duration)
    except (TypeError, ValueError):
        return False, "Duration must be a whole number of minutes."
    if val < 10:
        return False, "Duration must be at least 10 minutes."
    if val > 300:
        return False, "Duration must be 300 minutes or fewer."
    return True, ""


def validate_learning_objective(objective: str) -> tuple[bool, str]:
    """Learning objective must be non-empty and up to 500 characters."""
    stripped = objective.strip() if objective else ""
    if not stripped:
        return False, "Learning objective is required."
    if len(stripped) > 500:
        return False, "Learning objective must be 500 characters or fewer."
    return True, ""


def validate_difficulty(difficulty: str) -> tuple[bool, str]:
    """Difficulty must be one of the predefined levels."""
    if not difficulty or difficulty.strip() not in DIFFICULTY_LEVELS:
        return False, "Please select a valid difficulty level."
    return True, ""


def validate_question_type(question_type: str) -> tuple[bool, str]:
    """Question type must be one of the predefined options."""
    if not question_type or question_type.strip() not in QUESTION_TYPES:
        return False, "Please select a valid question type."
    return True, ""


def validate_num_questions(num_questions: int | float) -> tuple[bool, str]:
    """Number of questions must be an integer between MIN_QUESTIONS and MAX_QUESTIONS."""
    try:
        val = int(num_questions)
    except (TypeError, ValueError):
        return False, "Number of questions must be a whole number."
    if val < MIN_QUESTIONS:
        return False, f"Number of questions must be at least {MIN_QUESTIONS}."
    if val > MAX_QUESTIONS:
        return False, f"Number of questions must be {MAX_QUESTIONS} or fewer."
    return True, ""


def validate_student_name(name: str) -> tuple[bool, str]:
    """Student name is optional; if provided it must be max 50 characters."""
    if name and len(name.strip()) > 50:
        return False, "Student name must be 50 characters or fewer."
    return True, ""


def validate_student_text_field(text: str, field_name: str) -> tuple[bool, str]:
    """A required free-text student field must not be empty and max 500 characters."""
    stripped = text.strip() if text else ""
    if not stripped:
        return False, f"{field_name} is required."
    if len(stripped) > 500:
        return False, f"{field_name} must be 500 characters or fewer."
    return True, ""


def validate_mark(mark: int | float, field_name: str = "Mark") -> tuple[bool, str]:
    """A student mark must be a number between MIN_MARK and MAX_MARK (0–100)."""
    try:
        val = float(mark)
    except (TypeError, ValueError):
        return False, f"{field_name} must be a number."
    if val < MIN_MARK:
        return False, f"{field_name} must be {MIN_MARK} or higher."
    if val > MAX_MARK:
        return False, f"{field_name} must be {MAX_MARK} or lower."
    return True, ""


def validate_language(language: str) -> tuple[bool, str]:
    """Language must be chosen from the supported languages list."""
    if not language or language.strip() not in SUPPORTED_LANGUAGES:
        return False, "Please select a supported language."
    return True, ""


def validate_content_to_translate(content: str) -> tuple[bool, str]:
    """Content for translation must be non-empty and up to 2000 characters."""
    stripped = content.strip() if content else ""
    if not stripped:
        return False, "Please enter the content you want to translate."
    if len(stripped) > 2000:
        return False, "Content must be 2000 characters or fewer."
    return True, ""


def validate_learning_style(learning_style: str) -> tuple[bool, str]:
    """Learning style must be chosen from the predefined list."""
    if not learning_style or learning_style.strip() not in LEARNING_STYLES:
        return False, "Please select a valid learning style."
    return True, ""


def validate_credentials(api_key: str, project_id: str, url: str) -> tuple[bool, str]:
    """All three watsonx credential fields must be non-empty strings."""
    if not api_key or not api_key.strip():
        return False, "IBM watsonx API Key is required."
    if not project_id or not project_id.strip():
        return False, "IBM watsonx Project ID is required."
    if not url or not url.strip():
        return False, "IBM watsonx URL is required."
    return True, ""
