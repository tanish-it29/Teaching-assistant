"""
app.py — AI-Powered Teaching Assistant
Streamlit single-page application entry point.

Run with:  streamlit run app.py

The UI is organised into a sidebar (credentials + navigation) and
six feature sections selectable via the sidebar radio button.
"""

import os
import streamlit as st
from dotenv import load_dotenv

# Load .env file if it exists (credentials can also be entered in the sidebar)
load_dotenv()

from modules.config import (
    GRADE_LEVELS,
    DIFFICULTY_LEVELS,
    QUESTION_TYPES,
    LEARNING_STYLES,
    SUPPORTED_LANGUAGES,
    MAX_TOKENS_LESSON_PLAN,
    MAX_TOKENS_QUIZ,
    MAX_TOKENS_ASSESSMENT,
    MAX_TOKENS_RECOMMENDATION,
    MAX_TOKENS_MULTILINGUAL,
    MAX_TOKENS_ACTIVITY,
    MAX_TOKENS_RESOURCE,
    CONTENT_FILE,
    STUDENT_FILE,
    MIN_QUESTIONS,
    MAX_QUESTIONS,
)
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
from modules.prompt_builder import (
    build_lesson_plan_prompt,
    build_quiz_prompt,
    build_assessment_prompt,
    build_recommendation_prompt,
    build_multilingual_prompt,
    build_activity_prompt,
    build_resource_prompt,
)
from modules.storage import (
    append_record,
    make_content_record,
    make_student_record,
)
from modules.watsonx_client import (
    WatsonXClient,
    WatsonXConnectionError,
    WatsonXTimeoutError,
    WatsonXEmptyResponseError,
    WatsonXAPIError,
    load_credentials_from_env,
)

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="AI Teaching Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Session state initialisation
# ---------------------------------------------------------------------------

if "client" not in st.session_state:
    st.session_state["client"] = None
if "connected" not in st.session_state:
    st.session_state["connected"] = False


# ---------------------------------------------------------------------------
# Helper: run a generation and handle all errors in one place
# ---------------------------------------------------------------------------

def _generate(prompt: str, max_tokens: int) -> str | None:
    """
    Call the watsonx client, show a spinner, and handle all errors.
    Returns the generated text string on success, None on failure.
    """
    client: WatsonXClient | None = st.session_state.get("client")
    if client is None or not st.session_state.get("connected"):
        st.error(
            "⚠️ Not connected to IBM watsonx. "
            "Please enter your credentials in the sidebar and click **Connect**."
        )
        return None

    try:
        with st.spinner("✨ Generating with IBM watsonx Granite…"):
            return client.generate(prompt, max_tokens=max_tokens)
    except WatsonXConnectionError as exc:
        st.error(f"🔌 Connection error: {exc}")
    except WatsonXTimeoutError as exc:
        st.error(f"⏱️ Timeout: {exc}")
    except WatsonXEmptyResponseError as exc:
        st.error(f"📭 Empty response: {exc}")
    except WatsonXAPIError as exc:
        st.error(f"🚨 API error: {exc}")
    return None


def _show_output(label: str, text: str) -> None:
    """Display generated text in an expandable text area with a copy hint."""
    st.success("✅ Content generated successfully!")
    st.subheader(label)
    st.text_area(
        label="",
        value=text,
        height=400,
        label_visibility="collapsed",
        key=f"output_{label[:20]}",
        help="Select all (Ctrl+A / Cmd+A) then copy to use this content.",
    )
    st.caption(
        "💡 **Teacher reminder:** Review all AI-generated content before using it "
        "in your classroom. You are the professional — the AI is your assistant."
    )


def _collect_errors(checks: list[tuple[bool, str]]) -> list[str]:
    """Return a list of error messages from a list of (is_valid, message) tuples."""
    return [msg for ok, msg in checks if not ok]


# ---------------------------------------------------------------------------
# Sidebar: credentials + navigation
# ---------------------------------------------------------------------------

def render_sidebar() -> str:
    """Render the sidebar and return the selected navigation section name."""
    with st.sidebar:
        st.title("🎓 Teaching Assistant")
        st.caption("Powered by IBM watsonx / Granite")
        st.divider()

        # --- Credentials ---
        st.subheader("🔑 IBM watsonx Credentials")

        # Pre-fill from environment variables if available
        env_creds = load_credentials_from_env()

        api_key = st.text_input(
            "API Key",
            value=env_creds["api_key"],
            type="password",
            placeholder="Enter your IBM Cloud API key",
            help="Your IBM Cloud API key. Never shared or saved to disk.",
        )
        project_id = st.text_input(
            "Project ID",
            value=env_creds["project_id"],
            placeholder="Your watsonx.ai project ID",
        )
        url = st.text_input(
            "Endpoint URL",
            value=env_creds["url"],
            placeholder="https://us-south.ml.cloud.ibm.com",
        )

        if st.button("🔗 Connect", use_container_width=True, type="primary"):
            ok, msg = validate_credentials(api_key, project_id, url)
            if not ok:
                st.error(msg)
                st.session_state["connected"] = False
            else:
                try:
                    client = WatsonXClient(api_key=api_key, project_id=project_id, url=url)
                    client.connect()
                    st.session_state["client"] = client
                    st.session_state["connected"] = True
                    st.success("✅ Connected to IBM watsonx!")
                except WatsonXConnectionError as exc:
                    st.error(f"Connection failed: {exc}")
                    st.session_state["connected"] = False

        if st.session_state.get("connected"):
            st.success("🟢 Connected")
        else:
            st.warning("🔴 Not connected")

        st.divider()

        # --- Navigation ---
        st.subheader("📚 Features")
        section = st.radio(
            label="Select a feature",
            options=[
                "🗒️ Lesson Plan Generator",
                "📝 Quiz & Assessment",
                "👤 Student Performance Insights",
                "🌍 Multilingual Content",
                "🎯 Classroom Activities",
                "📦 Teaching Resources",
            ],
            label_visibility="collapsed",
        )

        st.divider()
        st.caption("Version 1.0 · College Project")

    return section  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# Section 1 — Lesson Plan Generator
# ---------------------------------------------------------------------------

def render_lesson_plan_section() -> None:
    st.header("🗒️ Lesson Plan Generator")
    st.write(
        "Enter your lesson details below and let the AI generate a structured lesson plan for you."
    )

    col1, col2 = st.columns(2)
    with col1:
        subject = st.text_input("Subject *", placeholder="e.g. Biology, Mathematics, History")
        topic = st.text_input("Topic *", placeholder="e.g. Photosynthesis, Fractions, World War II")
        grade_level = st.selectbox("Grade / Class Level *", GRADE_LEVELS, index=4)
    with col2:
        duration = st.number_input(
            "Duration (minutes) *", min_value=10, max_value=300, value=60, step=5
        )
        learning_objective = st.text_area(
            "Learning Objective *",
            placeholder="e.g. Students will be able to explain the process of photosynthesis.",
            height=120,
        )

    if st.button("📄 Generate Lesson Plan", type="primary", use_container_width=True):
        errors = _collect_errors([
            validate_subject(subject),
            validate_topic(topic),
            validate_grade_level(grade_level),
            validate_duration(duration),
            validate_learning_objective(learning_objective),
        ])
        if errors:
            for err in errors:
                st.error(err)
            return

        prompt = build_lesson_plan_prompt(
            subject=subject,
            topic=topic,
            grade_level=grade_level,
            duration_minutes=int(duration),
            learning_objective=learning_objective,
        )
        result = _generate(prompt, MAX_TOKENS_LESSON_PLAN)
        if result:
            _show_output("Generated Lesson Plan", result)
            append_record(
                CONTENT_FILE,
                make_content_record(
                    "lesson_plan",
                    {"subject": subject, "topic": topic, "grade": grade_level,
                     "duration": duration, "objective": learning_objective},
                    result,
                ),
            )


# ---------------------------------------------------------------------------
# Section 2 — Quiz & Assessment Generator
# ---------------------------------------------------------------------------

def render_quiz_section() -> None:
    st.header("📝 Quiz & Assessment Generator")
    st.write(
        "Generate quizzes or formal assessments with model answers. "
        "Select the question type that suits your needs."
    )

    col1, col2 = st.columns(2)
    with col1:
        topic = st.text_input("Topic *", placeholder="e.g. Algebra, The Water Cycle, Shakespeare")
        grade_level = st.selectbox("Grade / Class Level *", GRADE_LEVELS, index=4)
        difficulty = st.selectbox("Difficulty *", DIFFICULTY_LEVELS, index=1)
    with col2:
        num_questions = st.slider(
            "Number of Questions *", MIN_QUESTIONS, MAX_QUESTIONS, value=5
        )
        question_type = st.selectbox("Question Type *", QUESTION_TYPES)

    col_a, col_b = st.columns(2)

    with col_a:
        if st.button("📝 Generate Quiz", type="primary", use_container_width=True):
            errors = _collect_errors([
                validate_topic(topic),
                validate_grade_level(grade_level),
                validate_difficulty(difficulty),
                validate_num_questions(num_questions),
                validate_question_type(question_type),
            ])
            if errors:
                for err in errors:
                    st.error(err)
                return
            prompt = build_quiz_prompt(topic, grade_level, difficulty, num_questions, question_type)
            result = _generate(prompt, MAX_TOKENS_QUIZ)
            if result:
                _show_output("Generated Quiz", result)
                append_record(
                    CONTENT_FILE,
                    make_content_record(
                        "quiz",
                        {"topic": topic, "grade": grade_level, "difficulty": difficulty,
                         "num_questions": num_questions, "type": question_type},
                        result,
                    ),
                )

    with col_b:
        if st.button(
            "📋 Generate Assessment with Answers",
            type="secondary",
            use_container_width=True,
        ):
            errors = _collect_errors([
                validate_topic(topic),
                validate_grade_level(grade_level),
                validate_difficulty(difficulty),
                validate_num_questions(num_questions),
            ])
            if errors:
                for err in errors:
                    st.error(err)
                return
            prompt = build_assessment_prompt(topic, grade_level, difficulty, num_questions)
            result = _generate(prompt, MAX_TOKENS_ASSESSMENT)
            if result:
                _show_output("Generated Assessment with Model Answers", result)
                append_record(
                    CONTENT_FILE,
                    make_content_record(
                        "assessment",
                        {"topic": topic, "grade": grade_level, "difficulty": difficulty,
                         "num_questions": num_questions},
                        result,
                    ),
                )


# ---------------------------------------------------------------------------
# Section 3 — Student Performance Insights
# ---------------------------------------------------------------------------

def render_student_insights_section() -> None:
    st.header("👤 Student Performance Insights")
    st.info(
        "ℹ️ **Important:** The recommendations generated here are AI suggestions to support "
        "your professional judgment. They do not replace teacher observations or formal "
        "assessments. Always review before acting on any recommendation."
    )

    col1, col2 = st.columns(2)
    with col1:
        student_name = st.text_input(
            "Student Name (optional)",
            placeholder="e.g. Alex or Student A",
        )
        grade_level = st.selectbox("Grade / Class Level *", GRADE_LEVELS, index=4)
        subject = st.text_input("Subject *", placeholder="e.g. Mathematics")
        learning_style = st.selectbox("Preferred Learning Style *", LEARNING_STYLES)
    with col2:
        recent_mark_input = st.text_input(
            "Recent Assessment Mark (optional, 0–100)",
            placeholder="e.g. 68",
        )
        strengths = st.text_area(
            "Student Strengths *",
            placeholder="e.g. Good at problem solving, creative, works well in groups.",
            height=100,
        )
        weaknesses = st.text_area(
            "Areas Needing Improvement *",
            placeholder="e.g. Struggles with fractions, loses focus during long tasks.",
            height=100,
        )

    if st.button("💡 Generate Recommendations", type="primary", use_container_width=True):
        # Parse optional mark
        recent_mark: float | None = None
        mark_errors: list[tuple[bool, str]] = []
        if recent_mark_input.strip():
            try:
                recent_mark = float(recent_mark_input.strip())
                mark_errors = [validate_mark(recent_mark, "Recent Assessment Mark")]
            except ValueError:
                mark_errors = [(False, "Recent Assessment Mark must be a number.")]

        errors = _collect_errors([
            validate_student_name(student_name),
            validate_grade_level(grade_level),
            validate_subject(subject),
            validate_learning_style(learning_style),
            validate_student_text_field(strengths, "Student Strengths"),
            validate_student_text_field(weaknesses, "Areas Needing Improvement"),
        ] + mark_errors)

        if errors:
            for err in errors:
                st.error(err)
            return

        prompt = build_recommendation_prompt(
            student_name=student_name,
            grade_level=grade_level,
            subject=subject,
            strengths=strengths,
            weaknesses=weaknesses,
            learning_style=learning_style,
            recent_mark=recent_mark,
        )
        result = _generate(prompt, MAX_TOKENS_RECOMMENDATION)
        if result:
            _show_output("Personalized Learning Recommendations", result)
            append_record(
                STUDENT_FILE,
                make_student_record(
                    student_name=student_name,
                    grade_level=grade_level,
                    subject=subject,
                    strengths=strengths,
                    weaknesses=weaknesses,
                    learning_style=learning_style,
                    recent_mark=recent_mark,
                    ai_recommendation=result,
                ),
            )


# ---------------------------------------------------------------------------
# Section 4 — Multilingual Content Generator
# ---------------------------------------------------------------------------

def render_multilingual_section() -> None:
    st.header("🌍 Multilingual Content Generator")
    st.write(
        "Paste your educational content below, choose a target language, "
        "and the AI will translate and adapt it for that language."
    )

    content = st.text_area(
        "Educational Content to Translate *",
        placeholder="Paste your lesson explanation, instructions, or any educational text here…",
        height=200,
        max_chars=2000,
    )
    st.caption(f"{len(content)}/2000 characters used")

    target_language = st.selectbox("Target Language *", SUPPORTED_LANGUAGES)

    if st.button(
        f"🌐 Generate in {target_language}",
        type="primary",
        use_container_width=True,
    ):
        errors = _collect_errors([
            validate_content_to_translate(content),
            validate_language(target_language),
        ])
        if errors:
            for err in errors:
                st.error(err)
            return

        prompt = build_multilingual_prompt(content, target_language)
        result = _generate(prompt, MAX_TOKENS_MULTILINGUAL)
        if result:
            _show_output(f"Content in {target_language}", result)
            append_record(
                CONTENT_FILE,
                make_content_record(
                    "multilingual",
                    {"target_language": target_language,
                     "original_length": len(content)},
                    result,
                ),
            )


# ---------------------------------------------------------------------------
# Section 5 — Classroom Activity Generator
# ---------------------------------------------------------------------------

def render_activity_section() -> None:
    st.header("🎯 Classroom Activity Generator")
    st.write(
        "Describe your topic and class level and the AI will suggest engaging "
        "classroom activities with materials and step-by-step instructions."
    )

    col1, col2 = st.columns(2)
    with col1:
        subject = st.text_input("Subject (optional)", placeholder="e.g. Science, Art")
        topic = st.text_input("Topic *", placeholder="e.g. Ecosystems, Symmetry, Democracy")
    with col2:
        grade_level = st.selectbox("Grade / Class Level *", GRADE_LEVELS, index=4)

    if st.button("🎲 Suggest Classroom Activities", type="primary", use_container_width=True):
        errors = _collect_errors([
            validate_topic(topic),
            validate_grade_level(grade_level),
        ])
        if errors:
            for err in errors:
                st.error(err)
            return

        prompt = build_activity_prompt(topic=topic, grade_level=grade_level, subject=subject)
        result = _generate(prompt, MAX_TOKENS_ACTIVITY)
        if result:
            _show_output("Suggested Classroom Activities", result)
            append_record(
                CONTENT_FILE,
                make_content_record(
                    "activity",
                    {"subject": subject, "topic": topic, "grade": grade_level},
                    result,
                ),
            )


# ---------------------------------------------------------------------------
# Section 6 — Teaching Resource Generator
# ---------------------------------------------------------------------------

def render_resource_section() -> None:
    st.header("📦 Teaching Resource Generator")
    st.write(
        "Generate a complete set of teaching resources for any topic: key concepts, "
        "worked examples, practice questions, discussion questions, and a revision checklist."
    )

    col1, col2 = st.columns(2)
    with col1:
        subject = st.text_input("Subject (optional)", placeholder="e.g. Physics, English")
        topic = st.text_input("Topic *", placeholder="e.g. Forces and Motion, Poetry Analysis")
    with col2:
        grade_level = st.selectbox("Grade / Class Level *", GRADE_LEVELS, index=4)

    if st.button("📚 Generate Teaching Resources", type="primary", use_container_width=True):
        errors = _collect_errors([
            validate_topic(topic),
            validate_grade_level(grade_level),
        ])
        if errors:
            for err in errors:
                st.error(err)
            return

        prompt = build_resource_prompt(topic=topic, grade_level=grade_level, subject=subject)
        result = _generate(prompt, MAX_TOKENS_RESOURCE)
        if result:
            _show_output("Teaching Resources", result)
            append_record(
                CONTENT_FILE,
                make_content_record(
                    "resource",
                    {"subject": subject, "topic": topic, "grade": grade_level},
                    result,
                ),
            )


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Wire the sidebar navigation to the correct section renderer."""
    selected = render_sidebar()

    # App title banner
    st.markdown(
        """
        <div style='padding: 1rem 0 0.5rem 0;'>
            <h1 style='margin: 0;'>🎓 AI-Powered Teaching Assistant</h1>
            <p style='color: #666; margin: 0.3rem 0 0 0;'>
                Helping teachers save time and personalise learning with IBM watsonx / Granite.
                <strong>The AI is your assistant — you are always in control.</strong>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()

    # Route to the correct section
    if selected == "🗒️ Lesson Plan Generator":
        render_lesson_plan_section()
    elif selected == "📝 Quiz & Assessment":
        render_quiz_section()
    elif selected == "👤 Student Performance Insights":
        render_student_insights_section()
    elif selected == "🌍 Multilingual Content":
        render_multilingual_section()
    elif selected == "🎯 Classroom Activities":
        render_activity_section()
    elif selected == "📦 Teaching Resources":
        render_resource_section()


if __name__ == "__main__":
    main()
