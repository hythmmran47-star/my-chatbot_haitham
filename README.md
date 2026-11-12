# Medical Learning Chatbot | Arabic

An Arabic-first educational chatbot prototype for medical-learning questions, built with FastAPI, SQLAlchemy, SQLite, and a server-side Gemini integration.

## Current Features

- Arabic chat interface.
- FastAPI endpoint for submitting questions.
- SQLite persistence through SQLAlchemy.
- Conversation history retrieval by session ID.
- Server-side generative AI integration through an environment variable.
- Static HTML, CSS, and JavaScript frontend.

## Technology

Python 3.10+, FastAPI, Uvicorn, SQLAlchemy, SQLite, Pydantic, python-dotenv, Google Generative AI SDK, HTML, CSS, and JavaScript.

## Run Locally

1. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and set `GOOGLE_API_KEY`.
4. Start from the repository root:

   ```powershell
   uvicorn app.main:app --reload
   ```

5. Open `http://127.0.0.1:8000`.

## Environment Variables

| Variable | Purpose |
|---|---|
| `GOOGLE_API_KEY` | Private server-side API key. Never commit it. |
| `GEMINI_MODEL` | Optional model identifier; defaults to `gemini-1.5-flash`. |

## Security and Limitations

This is a learning prototype, not a medical device and not a substitute for qualified medical care. Do not enter real patient data. Before public deployment, implement authentication, authorization and ownership checks for chat sessions, request validation, rate limits, secure data retention, and privacy controls. The current history endpoint accepts a session ID without verifying the requesting user's ownership.

The former committed API key must be revoked in Google AI Studio or Google Cloud. Removing it from current files does not erase it from old Git commits; rotate the key and clean Git history before considering the repository sanitized.
