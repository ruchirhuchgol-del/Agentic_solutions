# AutonomousTradingCrew

Welcome to the AutonomousTradingCrew project. This advanced multi-agent AI system provides comprehensive stock market analysis and trading recommendations by leveraging specialized agents and custom financial tools.

##  Features

- **Multi-Agent System**: Four specialized AI agents working in concert
- **Enhanced Custom Financial Tools**: 
  - Financial Data Tool (real-time market data)
  - Financial Sentiment Tool (news sentiment analysis with FinBERT)
  - Risk Assessment Tool (VaR, stress testing, ML-based risk models)
  - Predictive Analytics Tool (LSTM, ARIMA, SARIMA models with adaptive quality)
- **Advanced ML Models**: 
  - FinBERT for financial sentiment analysis
  - Random Forest models for volatility and risk prediction
- **Multiple Interfaces**: CLI, Streamlit Web App, Jupyter Notebook
- **Comprehensive Analysis**: Market data, risk assessment, execution planning, and explainable reports
- **Adaptive Quality**: Dynamic adjustment to market conditions

##  Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

```bash
crewai install
```

Or alternatively:

```bash
pip install -r requirements.txt
```

###  Configuration

1. **Add your API keys** to the `.env` file:
   - `OPENAI_API_KEY` - Required for AI analysis
   - `SERPER_API_KEY` - Required for web search capabilities

2. **Customize agents and tasks** by modifying:
   - `src/autonomous_trading_crew/config/agents.yaml`
   - `src/autonomous_trading_crew/config/tasks.yaml`

##  Project Structure

```
autonomous_trading_crew/
├── README.md
├── requirements.txt
├── .env.example
├── pyproject.toml
├── setup.py
├── IMPLEMENTATION_SUMMARY.md
├── RESTRUCTURE_SUMMARY.md
├── ENHANCEMENT_SUMMARY.md
├── FINAL_VERIFICATION.md
├── src/
│   ├── autonomous_trading_crew/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── crew.py
│   │   ├── config/
│   │   │   ├── agents.yaml
│   │   │   └── tasks.yaml
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── market_intelligence_analyst.py
│   │   │   ├── risk_management_officer.py
│   │   │   ├── trade_execution_specialist.py
│   │   │   └── explainability_reporter.py
│   │   ├── tasks/
│   │   │   ├── __init__.py
│   │   │   ├── multi_modal_signal_synthesis.py
│   │   │   ├── risk_assessment_guardrail_check.py
│   │   │   ├── tax_optimized_execution_plan.py
│   │   │   └── decision_explanation_report.py
│   │   ├── tools/
│   │   │   ├── __init__.py
│   │   │   ├── financial_data_tool.py
│   │   │   ├── financial_sentiment_tool.py
│   │   │   ├── risk_assessment_tool.py
│   │   │   └── predictive_analytics_tool.py
│   │   ├── ui/
│   │   │   ├── __init__.py
│   │   │   ├── streamlit_app.py
│   │   │   └── cli.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── setup.py
│   ├── examples/
│   │   ├── __init__.py
│   │   └── interactive_analysis.ipynb
├── models/
│   ├── __init__.py
│   ├── financial_sentiment_model.py
│   ├── volatility_model.py
│   └── risk_factor_model.py
├── tests/
│   ├── __init__.py
│   ├── test_tools.py
│   ├── test_agents.py
│   ├── test_tasks.py
│   └── run_tests.py
├── docs/
│   ├── architecture.md
│   ├── development.md
│   ├── testing.md
│   └── user_guide.md
├── data/
├── logs/
└── examples/
```

##  Running the Project - Step by Step Execution Order

### 1. Initial Setup
```bash
# Clone the repository 
git clone <repository-url>
cd autonomous_trading_crew

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration
```bash
# Copy and configure environment variables
cp .env.example .env
# Edit .env to add your API keys
```

### 3. Model Initialization (First Run)
On the first execution, the system will automatically:
- Download the FinBERT model for sentiment analysis
- Train and save volatility prediction model
- Train and save risk factor classification model

This may take several minutes on the first run but will be cached for future use.

### 4. Command Line Interface

```bash
# Basic execution with default stock (AAPL)
crewai run

# Run analysis for a specific stock
python src/autonomous_trading_crew/main.py run TSLA

# Enhanced CLI with options
python src/autonomous_trading_crew/ui/cli.py AAPL --output result.json --verbose
```

### 5. Streamlit Web Interface

```bash
streamlit run src/autonomous_trading_crew/ui/streamlit_app.py
```

### 6. Jupyter Notebook

Open `src/autonomous_trading_crew/examples/interactive_analysis.ipynb` in Jupyter to run interactive analysis.

##  Understanding Your Crew

The autonomous_trading_crew Crew is composed of multiple AI agents, each with unique roles, goals, and tools:

### Agents

1. **Market Intelligence Analyst**: Fuses real-time news, social sentiment, and market information into actionable trading signals
2. **Risk Management Officer**: Enforces risk-adjusted return parameters and volatility guardrails
3. **Trade Execution Specialist**: Formulates detailed trade execution plans with tax efficiency considerations
4. **Explainability Reporter**: Generates comprehensive human-readable explanations for all trading decisions

### Custom Tools

- **Financial Data Tool**: Fetches real-time and historical market data from Yahoo Finance with technical indicators
- **Financial Sentiment Tool**: Analyzes sentiment of financial news with a specialized FinBERT model
- **Risk Assessment Tool**: Calculates Value at Risk (VaR), Conditional VaR, and other risk metrics using ML models
- **Predictive Analytics Tool**: Uses LSTM, ARIMA, and SARIMA models for price prediction with adaptive quality features

### Advanced ML Models

- **Financial Sentiment Model**: FinBERT-based sentiment analysis in `models/financial_sentiment_model.py`
- **Volatility Prediction Model**: Random Forest regressor in `models/volatility_model.py`
- **Risk Factor Model**: Risk classification model in `models/risk_factor_model.py`

##  Testing

To test the crew execution:

```bash
# Run all tests
python tests/run_tests.py

# Test specific components
python -m pytest tests/test_tools.py
python -m pytest tests/test_agents.py
python -m pytest tests/test_tasks.py
```

##  Success Metrics

- Complete a full analysis cycle within 5 minutes for a single stock
- Provide actionable trading signals with confidence levels
- Generate comprehensive risk assessments
- Create explainable reports for all decisions
- Adapt to changing market conditions with dynamic confidence adjustment

## Documentation

For detailed information about the system:

- **Implementation Summary**: `IMPLEMENTATION_SUMMARY.md`
- **Restructure Summary**: `RESTRUCTURE_SUMMARY.md`
- **Enhancement Summary**: `ENHANCEMENT_SUMMARY.md`
- **Architecture Guide**: `docs/architecture.md`
- **Development Guide**: `docs/development.md`
- **Testing Guide**: `docs/testing.md`
- **User Guide**: `docs/user_guide.md`

