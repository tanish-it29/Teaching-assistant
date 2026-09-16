# AI-Powered Teaching Assistant

A beginner-friendly Streamlit application that uses **IBM watsonx / Granite** to help teachers
create lesson plans, quizzes, assessments, personalized recommendations, multilingual content,
and classroom activities.

> **Note:** The AI is a teacher-support tool. All generated content should be reviewed by the
> teacher before use in the classroom.

---

## Prerequisites

- Python 3.10 or newer
- An IBM Cloud account with access to **watsonx.ai**
- A watsonx.ai **Project ID** and an **IBM Cloud API Key**

---

## Installation

```bash
# 1. Navigate to the project folder
cd teaching_assistant

# 2. (Recommended) Create and activate a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Configuring IBM watsonx Credentials

The application reads credentials from environment variables at runtime.
**Never put your API key in source code.**

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and fill in your real values:
   ```
   WATSONX_API_KEY=your-ibm-cloud-api-key
   WATSONX_PROJECT_ID=your-watsonx-project-id
   WATSONX_URL=https://us-south.ml.cloud.ibm.com
   ```
   - `WATSONX_API_KEY` — your IBM Cloud API key (create one at cloud.ibm.com → Manage → Access → API Keys)
   - `WATSONX_PROJECT_ID` — your watsonx.ai project ID (found in the project settings inside watsonx.ai)
   - `WATSONX_URL` — the regional endpoint (default: `https://us-south.ml.cloud.ibm.com`)

The application also lets you enter credentials directly in the sidebar at runtime
(useful for demos). Sidebar credentials take priority over `.env` values.

---

## Running the Application

```bash
streamlit run app.py
```

The app opens automatically in your browser at `http://localhost:8501`.

---

## Running the Tests

```bash
pytest tests/ -v
```

All tests mock the IBM watsonx API — no real API calls are made during testing.

---

## Project Structure

```
teaching_assistant/
├── app.py                        # Streamlit entry point
├── requirements.txt
├── .env.example                  # Credential template (copy to .env)
├── .env                          # Your real credentials (NOT in version control)
│
├── modules/
│   ├── config.py                 # Constants (model ID, grade list, languages...)
│   ├── validator.py              # Input validation functions
│   ├── prompt_builder.py         # Builds AI prompts for each feature
│   ├── watsonx_client.py         # IBM watsonx.ai API client
│   └── storage.py                # JSON read/write helpers
│
├── data/
│   ├── generated_content.json    # Auto-saved AI output history
│   └── student_records.json      # Auto-saved student performance entries
│
└── tests/
    ├── test_validator.py
    ├── test_prompt_builder.py
    └── test_storage.py
```

---

## Features

| Feature | Description |
|---|---|
| Lesson Plan Generator | Generates structured lesson plans from subject, topic, grade, duration, and objectives |
| Quiz & Assessment Generator | Generates MCQ or short-answer questions with answers |
| Student Performance Insights | Analyzes student data and provides personalized learning recommendations |
| Multilingual Content Generator | Adapts educational content into a selected target language |
| Classroom Activity Generator | Suggests classroom activities with materials and instructions |
| Teaching Resource Generator | Generates examples, discussion topics, practice questions, and revision points |
