# Usage Guide

This guide covers how to run the Hypothesis Generation Agent (HGA) via the command line, API server, and the main entry script.

## Command-Line Interface (CLI)
The CLI provides an interactive way to analyze a business problem.

- Command:
```bash
hga run
```
- Prompts for `Business Problem`, runs the crew, and prints a detailed report.

Other CLI commands:
- `hga train <iterations> <model_name>` — trains the crew for a given number of iterations.
- `hga test <n_iterations> <model_name>` — runs test executions for validation.

Implementation reference: `src/hypothesis_generation_agent/cli.py`

## API Server (FastAPI)
Run the API server for integration with external systems (e.g., Langflow):
```bash
uvicorn hypothesis_generation_agent.api_server:app --reload
```

- Health check:
  - `GET /health` → `{ "status": "healthy" }`
- Run crew:
  - `POST /run-crew`
  - Body:
    ```json
    { "business_problem": "Does the new campaign increase retention?" }
    ```
  - Response:
    ```json
    { "status": "success", "result": "... report text ..." }
    ```

Implementation reference: `src/hypothesis_generation_agent/api_server.py`

## Main Entry Script
Use the main script for local, interactive runs:
```bash
python run_app.py
```
- Prompts for a business problem (or uses a default if left blank).
- Prints a structured analysis including context, hypotheses, recommended test, and validation.

Implementation reference: `run_app.py`

## Configuration
- Environment variables are loaded from `.env`.
- See `docs/setup.md` for details.

## Knowledge Base (Optional)
- Place reference documents under `knowledge_base/`.
- Use `scripts/ingest_knowledge_base.py` if ingestion is required.