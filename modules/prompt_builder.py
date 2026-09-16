"""
prompt_builder.py — Builds AI prompt strings for each application feature.

Every function is a pure function: takes structured inputs, returns a prompt string.
No side effects. No API calls. Easy to unit-test.

Prompt convention used throughout:
  [Role]       — who the AI should act as
  [Context]    — the specific inputs (topic, grade, etc.)
  [Task]       — exactly what to generate
  [Format]     — how to structure the output
  [Constraint] — boundaries (grade-appropriate, education-focused, etc.)
"""


def build_lesson_plan_prompt(
    subject: str,
    topic: str,
    grade_level: str,
    duration_minutes: int,
    learning_objective: str,
) -> str:
    """Return a prompt that asks Granite to generate a structured lesson plan."""
    return (
        f"You are an experienced {subject} teacher creating a lesson plan for {grade_level} students.\n\n"
        f"Topic: {topic}\n"
        f"Duration: {duration_minutes} minutes\n"
        f"Learning Objective: {learning_objective}\n\n"
        f"Generate a structured lesson plan with the following clearly labelled sections:\n"
        f"1. Learning Objectives\n"
        f"2. Introduction / Hook (5–10 minutes)\n"
        f"3. Main Teaching Activities (with approximate times)\n"
        f"4. Guided Practice\n"
        f"5. Independent Practice\n"
        f"6. Assessment / Checking for Understanding\n"
        f"7. Closure / Summary\n"
        f"8. Resources Needed\n\n"
        f"Use clear headings and bullet points. Keep the language simple and practical.\n"
        f"Ensure all content is appropriate for {grade_level} and fits within {duration_minutes} minutes."
    )


def build_quiz_prompt(
    topic: str,
    grade_level: str,
    difficulty: str,
    num_questions: int,
    question_type: str,
) -> str:
    """Return a prompt that asks Granite to generate quiz questions."""
    if question_type == "Multiple Choice (MCQ)":
        format_instruction = (
            "Generate ONLY multiple-choice questions. "
            "For each question provide four options labelled A, B, C, D "
            "and clearly state the correct answer at the end of each question."
        )
    elif question_type == "Short Answer":
        format_instruction = (
            "Generate ONLY short-answer questions. "
            "For each question provide a concise model answer."
        )
    else:  # Mixed
        half = max(1, num_questions // 2)
        rest = num_questions - half
        format_instruction = (
            f"Generate {half} multiple-choice questions (each with options A, B, C, D and the correct answer) "
            f"followed by {rest} short-answer questions (each with a concise model answer)."
        )

    return (
        f"You are an educational assessment specialist creating a quiz for {grade_level} students.\n\n"
        f"Subject / Topic: {topic}\n"
        f"Difficulty: {difficulty}\n"
        f"Total Questions: {num_questions}\n\n"
        f"{format_instruction}\n\n"
        f"Number each question clearly (1, 2, 3 …).\n"
        f"Keep all questions appropriate for {grade_level} at a {difficulty} difficulty level.\n"
        f"Focus strictly on the topic: {topic}."
    )


def build_assessment_prompt(
    topic: str,
    grade_level: str,
    difficulty: str,
    num_questions: int,
) -> str:
    """Return a prompt that asks Granite to generate assessment questions with full model answers."""
    return (
        f"You are an experienced educator creating a formal assessment for {grade_level} students.\n\n"
        f"Topic: {topic}\n"
        f"Difficulty: {difficulty}\n"
        f"Number of Questions: {num_questions}\n\n"
        f"Generate {num_questions} assessment questions on the topic '{topic}'.\n"
        f"After each question, provide a detailed model answer that a teacher could use for marking.\n\n"
        f"Format each item as:\n"
        f"Q[number]: [question text]\n"
        f"Model Answer: [detailed answer]\n\n"
        f"Keep the language appropriate for {grade_level} students at a {difficulty} difficulty level."
    )


def build_recommendation_prompt(
    student_name: str,
    grade_level: str,
    subject: str,
    strengths: str,
    weaknesses: str,
    learning_style: str,
    recent_mark: float | None = None,
) -> str:
    """Return a prompt that asks Granite to generate personalized learning recommendations."""
    name_label = student_name.strip() if student_name and student_name.strip() else "the student"
    mark_line = f"Recent Assessment Mark: {recent_mark}%\n" if recent_mark is not None else ""

    return (
        f"You are a supportive educational advisor helping a teacher support their students.\n\n"
        f"Student: {name_label}\n"
        f"Grade Level: {grade_level}\n"
        f"Subject: {subject}\n"
        f"Identified Strengths: {strengths}\n"
        f"Areas Needing Improvement: {weaknesses}\n"
        f"Preferred Learning Style: {learning_style}\n"
        f"{mark_line}\n"
        f"Based on this information, provide personalized learning recommendations for the teacher "
        f"to use when supporting {name_label}. Include:\n"
        f"1. A brief summary of the student's current performance profile\n"
        f"2. Specific learning activities suited to their learning style ({learning_style})\n"
        f"3. Targeted practice suggestions for the weak areas\n"
        f"4. Ways to build on identified strengths\n"
        f"5. Simple resources or strategies the teacher can use in class or for homework\n\n"
        f"IMPORTANT: These are suggestions to support the teacher's professional judgment. "
        f"The teacher should review and adapt all recommendations before acting on them.\n"
        f"Keep the tone positive and constructive. Use clear, practical language."
    )


def build_multilingual_prompt(content: str, target_language: str) -> str:
    """Return a prompt that asks Granite to adapt educational content into a target language."""
    return (
        f"You are a bilingual educational translator.\n\n"
        f"Target Language: {target_language}\n\n"
        f"Original Educational Content:\n{content}\n\n"
        f"Translate and adapt the content above into {target_language}. "
        f"Preserve the educational meaning, structure, and tone. "
        f"Use vocabulary that is appropriate for a classroom setting. "
        f"If a direct translation would be unclear or culturally awkward, "
        f"adapt the phrasing so it is natural and easy for a {target_language}-speaking student to understand.\n"
        f"Provide ONLY the translated content — do not add commentary or notes."
    )


def build_activity_prompt(topic: str, grade_level: str, subject: str = "") -> str:
    """Return a prompt that asks Granite to suggest classroom activities."""
    subject_line = f"Subject: {subject}\n" if subject and subject.strip() else ""
    return (
        f"You are a creative and experienced teacher designing classroom activities.\n\n"
        f"{subject_line}"
        f"Topic: {topic}\n"
        f"Class Level: {grade_level}\n\n"
        f"Suggest 3 to 5 engaging classroom activities for this topic and class level. "
        f"For each activity include:\n"
        f"- Activity name\n"
        f"- Learning goal\n"
        f"- Required materials (keep it simple and low-cost)\n"
        f"- Step-by-step instructions (brief and clear)\n"
        f"- Approximate time required\n\n"
        f"Keep activities practical, age-appropriate for {grade_level}, "
        f"and achievable with standard classroom resources."
    )


def build_resource_prompt(topic: str, grade_level: str, subject: str = "") -> str:
    """Return a prompt that asks Granite to generate teaching resources."""
    subject_line = f"Subject: {subject}\n" if subject and subject.strip() else ""
    return (
        f"You are an experienced educator creating teaching resources.\n\n"
        f"{subject_line}"
        f"Topic: {topic}\n"
        f"Class Level: {grade_level}\n\n"
        f"Generate the following teaching resources for this topic:\n"
        f"1. Key Concepts Summary (bullet points, 5–8 points)\n"
        f"2. Worked Examples (2–3 clear examples showing how to apply concepts)\n"
        f"3. Practice Questions (5 questions without answers, for student practice)\n"
        f"4. Discussion Questions (3 thought-provoking questions for class discussion)\n"
        f"5. Revision Checklist (what students should know by the end of this topic)\n\n"
        f"Keep all content appropriate for {grade_level} students. "
        f"Use clear headings and concise language."
    )
