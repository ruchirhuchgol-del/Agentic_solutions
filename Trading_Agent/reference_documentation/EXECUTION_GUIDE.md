# Execution Guide

## Step-by-Step Execution Order

This guide provides a detailed walkthrough of how to execute the Autonomous Trading Crew project in the correct order.

## 1. Environment Setup

### Prerequisites
- Python 3.10-3.13
- pip or uv package manager
- At least 4GB free disk space for model downloads

### Installation Steps
```bash
# Navigate to project directory
cd autonomous_trading_crew

# Install dependencies
pip install -r requirements.txt

# Or using uv (faster)
uv pip install -r requirements.txt
```

## 2. Configuration

### Environment Variables
```bash
# Copy example configuration
cp .env.example .env

# Edit .env file to add your API keys
nano .env
```

Required API keys:
- `OPENAI_API_KEY`: For AI analysis
- `SERPER_API_KEY`: For web search capabilities

## 3. First-Time Model Initialization

On the first execution, the system will automatically:
1. Download the FinBERT model for sentiment analysis
2. Train and save the volatility prediction model
3. Train and save the risk factor classification model

This process may take 5-10 minutes depending on your internet connection.

## 4. Execution Methods

### Method 1: Using CrewAI CLI (Recommended for beginners)
```bash
# Run with default stock (AAPL)
crewai run

# Run with specific stock
crewai run TSLA
```

### Method 2: Using Main Script (More control)
```bash
# Run with default stock
python src/autonomous_trading_crew/main.py run

# Run with specific stock
python src/autonomous_trading_crew/main.py run MSFT
```

### Method 3: Using Enhanced CLI (Advanced features)
```bash
# Run with output file and verbose logging
python src/autonomous_trading_crew/ui/cli.py AAPL --output result.json --verbose

# Run with custom parameters
python src/autonomous_trading_crew/ui/cli.py TSLA --output tesla_analysis.json
```

### Method 4: Web Interface
```bash
# Start Streamlit web application
streamlit run src/autonomous_trading_crew/ui/streamlit_app.py
```

### Method 5: Jupyter Notebook
```bash
# Start Jupyter notebook server
jupyter notebook

# Open and run:
# src/autonomous_trading_crew/examples/interactive_analysis.ipynb
```

## 5. Understanding the Execution Flow

### Sequential Process
1. **Market Intelligence Analysis**
   - Agent: Market Intelligence Analyst
   - Tools: Financial Data Tool, Financial Sentiment Tool, Predictive Analytics Tool
   - Output: Market data, sentiment analysis, price predictions

2. **Risk Assessment**
   - Agent: Risk Management Officer
   - Tools: Risk Assessment Tool, Financial Data Tool
   - Output: Risk metrics, position sizing, stop-loss levels

3. **Execution Planning**
   - Agent: Trade Execution Specialist
   - Tools: Financial Data Tool
   - Output: Execution strategy, tax optimization

4. **Decision Reporting**
   - Agent: Explainability Reporter
   - Tools: All custom tools
   - Output: Comprehensive report with explanation

## 6. Monitoring and Troubleshooting

### Log Files
Check the `logs/` directory for detailed execution logs.

### Common Issues
1. **API Key Errors**: Verify keys in `.env` file
2. **Model Download Issues**: Check internet connection
3. **Memory Errors**: Close other applications to free memory
4. **Dependency Issues**: Reinstall with `pip install -r requirements.txt --force-reinstall`

### Performance Tips
- First run will be slower due to model downloads
- Subsequent runs will be faster due to caching
- Use the web interface for interactive exploration
- Use the CLI for batch processing

## 7. Advanced Usage

### Customizing Analysis
Modify configuration files:
- `src/autonomous_trading_crew/config/agents.yaml`
- `src/autonomous_trading_crew/config/tasks.yaml`

### Testing
Run the test suite:
```bash
# Run all tests
python tests/run_tests.py

# Run specific test modules
python -m pytest tests/test_tools.py
python -m pytest tests/test_agents.py
```

## 8. Output Interpretation

### JSON Output
The system generates structured JSON output containing:
- Market analysis data
- Risk assessment metrics
- Execution recommendations
- Confidence levels for all predictions

### Report Generation
The final output includes a comprehensive markdown report with:
- Executive summary
- Detailed analysis
- Risk considerations
- Execution plan
- Decision rationale

## 9. Best Practices

### For Accurate Analysis
- Run during market hours for real-time data
- Use actively traded stocks with sufficient history
- Review multiple stocks for portfolio diversification

### For Performance Optimization
- Use the CLI for automated batch processing
- Use the web interface for interactive exploration
- Save results to files for historical comparison

### For Risk Management
- Review risk assessments carefully
- Consider position sizing recommendations
- Monitor stop-loss and take-profit levels
- Diversify investments across multiple stocks