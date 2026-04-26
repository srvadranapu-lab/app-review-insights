# App Review Insights Analyser

An automated weekly system that analyzes public App Store and Google Play reviews for fintech products and generates insight reports delivered via Google Workspace.

## Features

- Automated review ingestion from App Store and Google Play
- AI-powered theme clustering and insight generation
- Weekly reports delivered to Google Docs and Gmail
- Idempotent runs with audit trails
- MCP-based Google Workspace integration

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your GROQ_API_KEY
```

## Usage

### FastAPI Server

Start the FastAPI server:

```bash
python -m app.main
```

The server will be available at `http://localhost:8000`

Health check endpoint:
```bash
curl http://localhost:8000/health
```

### CLI

Run the analysis pipeline:

```bash
python -m app.cli run
```

## Project Structure

```
app-review-insights/
├── docs/                    # Documentation
├── app/                     # Main application
│   ├── __init__.py
│   ├── main.py             # FastAPI application
│   ├── config.py           # Configuration
│   ├── database.py         # SQLite database
│   ├── models.py           # Pydantic models
│   └── cli.py              # Command line interface
├── data/                   # SQLite database files
├── .env                    # Environment variables
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Development

The project is structured to support phased development:

- **Phase 0**: Foundation (current)
- **Phase 1**: Review ingestion
- **Phase 2**: Data cleaning
- **Phase 3**: AI insights generation
- **Phase 4**: Report generation
- **Phase 5**: Google Workspace integration
- **Phase 6**: Email delivery
- **Phase 7**: Automation

## Architecture

The system follows a modular architecture:

1. **Ingestion Layer**: Collects reviews from app stores
2. **Processing Layer**: Cleans and filters data
3. **LLM Layer**: Uses Groq for insight generation
4. **Report Generator**: Creates structured reports
5. **MCP Layer**: Handles Google Workspace integration

For detailed architecture information, see `docs/architecture.md`.
