# Hypothesis Generation Agent (HGA)

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](link/to/your/ci)
[![Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen.svg)](link/to/coverage/report)

The Hypothesis Generation Agent (HGA) is a multi-agent AI system designed to automate the foundational, time-consuming task of formulating statistical hypotheses for data science projects. By leveraging the power of CrewAI, it translates natural language business problems into rigorous, well-reasoned hypotheses, recommends appropriate statistical tests, and provides a clear rationale—accelerating the journey from problem to insight.

## 🚀 Key Features

- **Multi-Agent Collaboration:** Specialized AI agents (Context Extractor, Hypothesis Generator, Test Recommender, Validator, Reviewer) collaborate to produce high-quality outputs.
- **Knowledge-Grounded Reasoning:** Uses a curated knowledge base for consistent, standards-aligned recommendations.
- **Statistical Validation:** Peer-review checks ensure logical consistency between hypotheses and tests.
- **Interactive Clarification:** Detects ambiguity and asks clarifying questions when needed.
- **Modular & Extensible:** Clean architecture; easily add agents, tasks, or tools.

## 🏃‍♂️ Quick Start

Get HGA running in minutes.

**1. Setup Environment**
```bash
python -m venv venv
venv\\Scripts\\activate  # Windows
# or
source venv/bin/activate    # macOS/Linux
pip install -r requirements.txt
```

**2. Configure `.env`**
Create and edit `.env` in the project root:
```env
OPENAI_API_KEY=sk-...optional-key...
LLM_MODEL=default-model
LLM_TEMPERATURE=0.7
LOG_LEVEL=INFO
```

**3. Run**
- Main entry:
```bash
python run_app.py
```
- CLI:
```bash
hga run
```
- API server:
```bash
uvicorn hypothesis_generation_agent.api_server:app --reload
```

## 📚 Documentation
- Setup: `docs/setup.md`
- Architecture: `docs/architecture.md`
- Usage: `docs/usage.md`
- Testing: `docs/testing.md`
- Troubleshooting: `docs/troubleshooting.md`

## 🗂️ Project Structure
```
├── run_app.py
├── src/
│   └── hypothesis_generation_agent/
│       ├── agents/
│       ├── tasks/
│       ├── tools/
│       ├── crew.py
│       ├── crew_alternate.py
│       ├── api_server.py
│       ├── cli.py
│       └── config/
├── docs/
│   ├── setup.md
│   ├── architecture.md
│   ├── usage.md
│   ├── testing.md
│   └── troubleshooting.md
├── knowledge_base/
├── scripts/
└── tests/
```

## 🧪 Testing
```bash
pytest --cov=hypothesis_generation_agent -v
```
Or use `./scripts/run_tests.sh`.

## 🤝 Contributing
- Open issues and PRs are welcome.
- Follow coding style consistent with existing modules.

## 📄 License
MIT