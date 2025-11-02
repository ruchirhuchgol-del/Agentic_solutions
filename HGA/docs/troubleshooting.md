# Troubleshooting

This guide lists common issues and how to resolve them when working with HGA.

## Authentication Errors
- Symptom: `litellm.exceptions.AuthenticationError` or "Incorrect API key provided".
- Cause: Missing or invalid API key in `.env`.
- Fix:
  - Set `OPENAI_API_KEY` in `.env` to a valid key.
  - Ensure the environment is loading `.env` (e.g., `dotenv` is installed and invoked).
  - For development, consider mock mode using the `run_app.py` implementation.

## Output Parsing Errors
- Symptom: `ValueError: Could not parse LLM output` or prompt variables missing (e.g., `agent_scratchpad`).
- Cause: Prompt template not aligned with agent expectations.
- Fix:
  - Ensure prompts include required variables like `{agent_scratchpad}` for ReAct-style agents.
  - Adjust the agent executor configuration (`handle_parsing_errors=True`) if applicable.

## Missing Module Errors
- Symptom: `ModuleNotFoundError: No module named 'crewai.utilities.schema_converter'`.
- Cause: Importing modules that are not part of the installed package version.
- Fix:
  - Remove or replace the import (e.g., it was removed from `crew_alternate.py`).
  - Update dependencies with `pip install -r requirements.txt`.

## Environment Not Loaded
- Symptom: Variables from `.env` are not recognized.
- Fix:
  - Call `load_dotenv()` early in the entry point.
  - Verify `.env` is in the project root.

## Windows-Specific Path/Permission Issues
- Symptom: File deletion or path resolution failures.
- Fix:
  - Run terminal with appropriate permissions.
  - Avoid deleting files to the recycle bin from scripts; prefer direct deletion.

## API Server CORS Issues
- Symptom: Browser or external client cannot call the API.
- Fix:
  - Confirm CORS middleware is configured to allow origins as needed.
  - In production, restrict `allow_origins` to the actual client URL.

## Logging and Debugging
- Increase verbosity by setting `LOG_LEVEL=DEBUG` in `.env`.
- Check console and log outputs for stack traces.