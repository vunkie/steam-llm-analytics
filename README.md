# Steam Library Analytics

A Python application that uses AI to analyze your Steam game library through natural language queries.

## How it works

1. Enter your Steam vanity URL or Steam ID
2. The app fetches your library data from the Steam API and stores it locally
3. Ask questions about your library in natural language (Portuguese)
4. A local LLM (Qwen2.5-Coder) generates the SQL query, and Gemini formats the response

## Tech Stack

- **Python** — core language
- **Steam Web API** — game library data
- **SQLite** — local database (via SQLAlchemy)
- **SQLAlchemy** — ORM and database abstraction
- **llama-cpp-python** — local LLM inference (no API cost for SQL generation)
- **Google Gemini API** — natural language response formatting
- **Streamlit** — web interface

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/steam-llm-analytics.git
cd steam-llm-analytics
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download the local LLM model

Download the `qwen2.5-coder-1.5b-instruct-q4_k_m.gguf` model from Hugging Face:

> https://huggingface.co/Qwen/Qwen2.5-Coder-1.5B-Instruct-GGUF

Place the file inside a `models/` folder in the project root:

```
steam-llm-analytics/
└── models/
    └── qwen2.5-coder-1.5b-instruct-q4_k_m.gguf
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```
STEAM_API_KEY=your_steam_api_key
STEAM_ID=your_steam_id
DATABASE_URL=sqlite:///steam_data.db
GEMINI_API_KEY=your_gemini_api_key
```

- Steam API key: https://steamcommunity.com/dev/apikey
- Gemini API key: https://aistudio.google.com/apikey

### 6. Run the app

```bash
streamlit run app.py
```

## Usage

- Enter your Steam vanity URL (e.g. `yourname`) or full profile URL
- Wait for your library to load
- Ask questions in Portuguese, for example:
  - *"Quais os 5 jogos mais jogados no geral?"*
  - *"Quantas horas joguei no Steam Deck?"*
  - *"Quais jogos joguei mais de 100 horas?"*

## Preview

![Steam Library Analytics](screenshot.png)

## Notes

- The local LLM runs entirely on your machine — no API calls for SQL generation
- Gemini free tier is used only for response formatting (1 request per question)
- The database is reset every time a new Steam ID is loaded
- Prompts must be in Portuguese for best results with the local model