"""
config.py — Application-wide constants.

Edit this file to change supported languages, grade levels, or the watsonx model.
All other modules import their constants from here.
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# IBM watsonx / Granite model
# ---------------------------------------------------------------------------

MODEL_ID: str = "ibm/granite-3-8b-instruct"

# Regional endpoint — overridden by WATSONX_URL env variable at runtime
DEFAULT_WATSONX_URL: str = "https://us-south.ml.cloud.ibm.com"

# ---------------------------------------------------------------------------
# Token limits per feature (controls response length)
# ---------------------------------------------------------------------------

MAX_TOKENS_LESSON_PLAN: int = 1200
MAX_TOKENS_QUIZ: int = 900
MAX_TOKENS_ASSESSMENT: int = 900
MAX_TOKENS_RECOMMENDATION: int = 700
MAX_TOKENS_MULTILINGUAL: int = 1300
MAX_TOKENS_ACTIVITY: int = 800
MAX_TOKENS_RESOURCE: int = 800

# ---------------------------------------------------------------------------
# Grade / class levels
# ---------------------------------------------------------------------------

GRADE_LEVELS: list[str] = [
    "Grade 1", "Grade 2", "Grade 3", "Grade 4",
    "Grade 5", "Grade 6", "Grade 7", "Grade 8",
    "Grade 9", "Grade 10", "Grade 11", "Grade 12",
    "University / College",
]

# ---------------------------------------------------------------------------
# Quiz / assessment options
# ---------------------------------------------------------------------------

DIFFICULTY_LEVELS: list[str] = ["Easy", "Medium", "Hard"]

QUESTION_TYPES: list[str] = [
    "Multiple Choice (MCQ)",
    "Short Answer",
    "Mixed (MCQ + Short Answer)",
]

MIN_QUESTIONS: int = 1
MAX_QUESTIONS: int = 20

# ---------------------------------------------------------------------------
# Student performance
# ---------------------------------------------------------------------------

LEARNING_STYLES: list[str] = [
    "Visual",
    "Auditory",
    "Reading / Writing",
    "Hands-on / Kinesthetic",
]

MIN_MARK: float = 0.0
MAX_MARK: float = 100.0

# ---------------------------------------------------------------------------
# Multilingual support
# Granite handles these languages reliably.
# ---------------------------------------------------------------------------

SUPPORTED_LANGUAGES: list[str] = [
    "English",
    "French",
    "Spanish",
    "German",
    "Portuguese",
    "Arabic",
    "Japanese",
    "Korean",
    "Chinese (Simplified)",
    "Afrikaans",
    "Zulu",
    "Xhosa",
]

# ---------------------------------------------------------------------------
# Local data persistence (JSON files)
# ---------------------------------------------------------------------------

# Resolve paths relative to this file so they work from any working directory
_BASE_DIR: Path = Path(__file__).resolve().parent.parent
DATA_DIR: Path = _BASE_DIR / "data"
CONTENT_FILE: Path = DATA_DIR / "generated_content.json"
STUDENT_FILE: Path = DATA_DIR / "student_records.json"
