# FinancialReconciliationAutomation Crew

Welcome to the FinancialReconciliationAutomation Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.


## Repository Structure
financial_reconciliation_automation_v1_crewai-project/
├── data/
│ ├── processed/
│ │ ├── reports/
│ │ │ ├── matching_results.json
│ │ │ └── reconciliation_report.txt
│ │ └── processed data files
│ └── sample/
│ ├── transactions.csv
│ └── invoices.csv
├── docs/
│ ├── architecture.md
│ ├── setup.md
│ ├── api_reference.md
│ └── user_guide.md
├── examples/
│ ├── financial_reconciliation_example.py
│ ├── langchain_tools_example.py
│ ├── run_reconciliation.py
│ ├── run_ui.py
│ └── ui_example.py
├── scripts/
│ ├── deploy.sh
│ ├── run_tests.sh
│ └── setup_env.sh
├── src/
│ └── financial_reconciliationautomation/
│ ├── chains/
│ │ ├── matchingchain.py
│ │ ├── reporting_chain.py
│ │ └── validation_chain.py
│ ├── config/
│ │ ├── agents.yaml
│ │ └── tasks.yaml
│ ├── schemas/
│ │ ├── report.py
│ │ └── transaction.py
│ ├── tools/
│ │ ├── financial_tools.py
│ │ └── langchain_tools.py
│ ├── ui/
│ │ ├── components.py
│ │ ├── streamlit_app.py
│ │ ├── test_components.py
│ │ ├── test_ui.py
│ │ └── utils.py
│ ├── utils/
│ │ ├── data_loader.py
│ │ ├── formatters.py
│ │ └── validators.py
│ ├── crew.py
│ └── main.py
├── tests/
│ ├── fixtures/
│ │ ├── sample_invoices.json
│ │ └── sample_transactions.json
│ ├── test_agents.py
│ ├── test_chains.py
│ ├── test_integration.py
│ ├── test_langchain_tools.py
│ ├── test_tasks.py
│ └── test_tools.py
├── .env
├── .gitignore
├── README.md
├── configurations.json
├── pyproject.toml
└── reconciliation_report.md



## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```

### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/financial_reconciliation_automation/config/agents.yaml` to define your agents
- Modify `src/financial_reconciliation_automation/config/tasks.yaml` to define your tasks
- Modify `src/financial_reconciliation_automation/crew.py` to add your own logic, tools and specific args
- Modify `src/financial_reconciliation_automation/main.py` to add custom inputs for your agents and tasks

## Running the Project

### Command Line Interface

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the financial_reconciliation_automation Crew, assembling the agents and assigning them tasks as defined in your configuration.

### Web Interface

This project also includes a Streamlit web interface for easier interaction:

```bash
$ crewai ui
```

Or directly with Python:

```bash
$ streamlit run src/financial_reconciliation_automation/ui/streamlit_app.py
```

The web interface provides:
- Interactive configuration of reconciliation parameters
- Real-time progress monitoring
- Visual dashboards for results
- Downloadable reports and logs

## Understanding Your Crew

The financial_reconciliation_automation Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the FinancialReconciliationAutomation Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.