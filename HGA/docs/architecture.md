# Architecture Overview

This document describes the architecture of the Hypothesis Generation Agent (HGA), its main components, and how they interact.

## High-Level Design
HGA follows a modular, multi-agent architecture powered by CrewAI. Each agent specializes in a stage of the hypothesis-generation workflow, and tasks orchestrate agent execution.

- Agents live in `src/hypothesis_generation_agent/agents/`
- Tasks live in `src/hypothesis_generation_agent/tasks/`
- Tools live in `src/hypothesis_generation_agent/tools/`
- Crew composition and orchestration are defined in `src/hypothesis_generation_agent/crew.py` and `src/hypothesis_generation_agent/crew_alternate.py`
- Configuration and logging utilities live in `src/hypothesis_generation_agent/config/`
- Entry points include the CLI (`src/hypothesis_generation_agent/cli.py`), API server (`src/hypothesis_generation_agent/api_server.py`), and `run_app.py`

## Core Components

- **Agents** — Specialized roles that perform reasoning steps.
  - `ContextExtractor`: Parses the business problem to identify metric, groups, and assumptions.
  - `HypothesisGenerator`: Produces H₀/H₁ with proper statistical notation.
  - `TestRecommender`: Selects appropriate statistical tests.
  - `StatisticalValidator`: Validates cross-consistency and flags issues.
  - `Reviewer`: Synthesizes outputs into a final report.

- **Tasks** — Declarative units describing what an agent should do.
  - Located under `src/hypothesis_generation_agent/tasks/`
  - Example tasks include: `ExtractContextTask`, `GenerateHypothesesTask`, `RecommendTestTask`, `ValidateConsistencyTask`, `ReviewOutputTask`, `StoreHypothesisTask`, `RefineHypothesisTask`.

- **Tools** — Utilities used by agents to read files or perform auxiliary operations.
  - Example: `CustomFileReadTool` wrapping `crewai_tools.FileReadTool` for robust file access.

- **Crew** — Orchestrates agents and tasks.
  - Defined in `crew.py` and `crew_alternate.py`.
  - Uses the `LLM` interface and configuration defaults from `config/__init__.py`.

## Data Flow
1. The user provides a `business_problem` via CLI, API, or `run_app.py`.
2. The crew kicks off the workflow, executing tasks in order.
3. Agents produce intermediate artifacts (context, hypotheses, test selection).
4. The reviewer consolidates the artifacts into a final, formatted report.

## Configuration
- Defaults are defined in `src/hypothesis_generation_agent/config/__init__.py`.
- Environment variables (loaded via `dotenv`) control runtime settings like model, temperature, and logging.
- A YAML-based `llm_config.yaml` provides additional provider configuration options.

## Entry Points
- **CLI**: `hga run` → prompts for `business_problem` and prints results.
- **API**: `POST /run-crew` → accepts JSON `{ business_problem }` and returns the result.
- **Main**: `python run_app.py` → interactive prompt in the terminal.

## Testing and Validation
- Unit and integration tests are located under `tests/`.
- Example tests: `tests/integration/test_crew.py` and `tests/integration/test_workflow.py`.

## Notes on LLM Integration
- The project supports running with a mock LLM for development environments where an API key is not available.
- For production, set `OPENAI_API_KEY` and provider-specific settings via `.env` and configuration files.