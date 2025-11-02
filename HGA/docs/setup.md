# Setup and Configuration

This guide covers environment setup, dependency installation, and configuration for the Hypothesis Generation Agent (HGA).

## Requirements
- Python 3.10+
- Windows, macOS, or Linux
- Optional: A valid API key for your chosen LLM provider

## 1. Create a Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

## 2. Install Dependencies
```bash
pip install -r requirements.txt
```

If you plan to run the FastAPI server:
```bash
pip install fastapi uvicorn
```

## 3. Environment Variables
Configuration is managed via a `.env` file in the project root.

### Core variables
- `OPENAI_API_KEY` — API key for the LLM provider (optional if using mock mode)
- `LLM_MODEL` — default model identifier (e.g., provider-specific string)
- `LLM_TEMPERATURE` — generation temperature (e.g., `0.7`)
- `LOG_LEVEL` — logging verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`)

### Example `.env`
```env
# LLM Provider Configuration
OPENAI_API_KEY=sk-...your-key...

# LLM Defaults
LLM_MODEL=default-model
LLM_TEMPERATURE=0.7

# Application Settings
LOG_LEVEL=INFO
```

## 4. Optional Knowledge Base Ingestion
If you plan to use the knowledge base:
```bash
python scripts/ingest_knowledge_base.py
```

## 5. Verifying Installation
Run the main entry:
```bash
python run_app.py
```

Run the CLI (installed as an entrypoint via the package):
```bash
hga run
```

Run the API server:
```bash
uvicorn hypothesis_generation_agent.api_server:app --reload
```