[README.md](https://github.com/user-attachments/files/33271362/README.md)
# AI Mock Interview Assistant


An AI-powered mock interview platform that evaluates candidate answers using a hybrid stack of local NLP analysis (spaCy + TextBlob) and the Google Gemini API. It provides real-time scoring, speech pacing analysis, sentiment detection, STAR-framework coaching, audio transcription, progress dashboards, and full interview-simulation summaries.

## Features

- **Multi-domain question bank** — 600 curated interview questions across 6 domains (100 each).
- **Multi-dimensional response evaluation** — composite score (0–100) built from:
  - Keyword & concept coverage (25%)
  - Technical depth & substance (35%)
  - Communication structure (20%)
  - Delivery & confidence (20%)
- **Deep NLP analysis** for every answer:
  - spaCy-powered keyword matching and lemmatization
  - Filler-word & hesitation detection (fluency metrics)
  - TextBlob sentiment and tone classification
  - Confidence scoring with delivery advice
  - Speech pacing (WPM), filler rate (FPM), and delivery energy
  - STAR (Situation, Task, Action, Result) framework alignment
  - Quantitative impact / metrics detection
  - Response relevance & prompt alignment
- **Gemini LLM assessment** — executive feedback, strengths, improvements, a benchmark model answer, and a probing follow-up question, with automatic multi-model fallback.
- **Intelligent local fallback** — the app keeps working even if the Gemini API is down or overloaded (`engine: "local-nlp"`).
- **Audio answers** — record your answer and get verbatim speech-to-text transcription plus delivery metrics.
- **Streamed interviewer reaction** — server-sent events (SSE) play the interviewer's live 2-sentence reaction while you wait.
- **Practice history** — searchable, filterable session history with JSON export and clear option.
- **Progress dashboard** — average/best scores, domain mastery, skill breakdown, sentiment distribution, WPM averages, trend lines, and a **Readiness Index** (0–100) with ranking tiers.
- **Interview simulation summary** — aggregate a round of sessions into a hiring recommendation (STRONG HIRE / HIRE / LEANING HIRE / NO HIRE).
- **Custom questions** — add your own questions to any domain (with duplicate protection).

## Tech Stack

- **Language:** Python 3.10+
- **Web framework:** Flask
- **NLP:** spaCy (`en_core_web_sm`), TextBlob, custom regex heuristics
- **AI / Speech-to-Text:** Google Gemini (`google-genai`) with model fallback chain
- **Storage:** Flat JSON files (`questions.json`, `history.json`)
- **Frontend:** Server-rendered HTML/CSS/JS templates with a dark "glassmorphism" UI

## Project Structure

```
mock_interview_app/
├── app.py                     # Flask app: routes, evaluation API, history, dashboard, simulation
├── nlp_engine.py              # NLP analysis pipeline + Gemini evaluation & transcription
├── questions.json             # Question bank (600 questions)
├── questions.json.bak         # Backup of original question bank
├── history.json               # Persisted practice-session records
├── build_full_bank.py         # Assembles + validates the 600-question bank
├── generate_questions_bank.py # Legacy question-bank generator
├── test_app.py                # unittest suite for routes & APIs
├── requirements.txt
├── .env                       # GEMINI_API_KEY (secret — don't commit)
├── templates/
│   ├── index.html             # Main practice interface
│   ├── dashboard.html         # Progress dashboard
│   └── history.html           # Session history
├── static/
│   ├── logo.svg
│   └── wallpaper.jpg
└── question_data/
    ├── se_builder.py          # Software Engineering (se_16..se_100)
    ├── ds_builder.py          # Data Science
    ├── pm_builder.py          # Product Management
    ├── bh_builder.py          # Behavioral
    ├── py_builder.py          # Python Developer
    └── fs_builder.py          # Forensic Science
```

## Domains

| Key                    | Label                 | Questions |
|------------------------|-----------------------|-----------|
| `software_engineering` | Software Engineering  | 100       |
| `data_science`         | Data Science          | 100       |
| `product_management`   | Product Management    | 100       |
| `behavioral`           | Behavioral            | 100       |
| `python_developer`     | Python Developer      | 100       |
| `forensic_science`     | Forensic Science      | 100       |

## Installation

1. **Clone the repository**

   ```
   git clone <your-repo-url>
   cd mock_interview_app
   ```

2. **Create and activate a virtual environment** (recommended)

   ```
   python -m venv venv
   .\venv\Scripts\activate        # Windows
   source venv/bin/activate       # macOS/Linux
   ```

3. **Install dependencies**

   ```
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

4. **Set your Gemini API key**

   Create a `.env` file in the project root:

   ```
   GEMINI_API_KEY=your_key_here
   ```

   Get a free key at [Google AI Studio](https://aistudio.google.com/app/apikey). The app refuses to start without it.

5. **(Optional) Rebuild the question bank**

   ```
   python build_full_bank.py
   ```

## Running the App

```
python app.py
```

Then open <http://localhost:5000>.

## Running Tests

```
python test_app.py
```

The test suite covers page routes, the questions API, random-question picker, custom-question submission, full response evaluation (with NLP metrics), simulation summaries, dashboard stats, and history export.

## API Overview

| Method | Endpoint                     | Description                                         |
|--------|------------------------------|-----------------------------------------------------|
| GET    | `/`                          | Main practice page                                  |
| GET    | `/dashboard`                 | Progress dashboard                                  |
| GET    | `/history`                   | Session history page                                |
| GET    | `/api/questions/<domain>`    | Questions for a domain (optional `?difficulty=`)    |
| GET    | `/api/questions/random`      | Random question (optional `?domain=`)               |
| POST   | `/api/questions/add`         | Add a custom question                               |
| POST   | `/api/evaluate`              | Evaluate a candidate response                       |
| POST   | `/api/stream_feedback`       | Stream interviewer reaction (SSE)                   |
| POST   | `/api/transcribe_audio`      | Speech-to-text transcription of an audio upload     |
| GET    | `/api/history`               | Practice history (`?domain=`, `?q=` filter)         |
| POST   | `/api/history/clear`         | Clear all history                                   |
| GET    | `/api/history/export`        | Download history as JSON                            |
| GET    | `/api/dashboard/stats`       | Aggregated dashboard statistics                     |
| POST   | `/api/simulation/summary`    | Hiring recommendation for a round of sessions       |

### Example: Evaluate a response

```json
POST /api/evaluate
{
  "domain": "software_engineering",
  "question_id": "se_1",
  "question_text": "Explain SOLID principles",
  "expected_keywords": ["single responsibility", "dependency inversion", "open closed"],
  "response": "In our team I applied Single Responsibility and Dependency Inversion to build modular payment adapters...",
  "duration_seconds": 45
}
```

## Scoring & Metrics

Composite score weights:

1. **Keyword coverage** — 25%: ratio of expected concepts found in your answer
2. **Technical depth** — 35%: Gemini technical-depth rating (0–100)
3. **Communication structure** — 20%: answer length suitability + low filler usage
4. **Delivery confidence** — 20%: assertiveness, fillers, hesitations, sentiment

Readiness tiers on the dashboard:

- **85+** Staff / Principal Caliber
- **70–84** Senior Engineer Ready
- **50–69** Mid-Level Competitive
- **<50** Foundational Preparation

## Notes & Limitations

- Audio duration is automatically parsed only for WAV uploads; otherwise it is estimated from a ~135 WPM baseline.
- SSL/TLS cert verification for API calls may be OS-dependent on Windows.
- `history.json` grows with each response evaluation — clear it periodically from the UI or via `POST /api/history/clear`.

