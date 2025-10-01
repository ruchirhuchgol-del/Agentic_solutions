# User Guide

## Getting Started

### Prerequisites
- Python 3.10-3.13
- API keys for OpenAI and SerperDev
- Internet connection for data retrieval

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd autonomous_trading_crew

# Install dependencies
pip install -r requirements.txt
```

### Configuration
1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` to add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   SERPER_API_KEY=your_serper_api_key_here
   ```

## Running the System

### Command Line Interface
```bash
# Run analysis for a specific stock
python src/autonomous_trading_crew/main.py run AAPL

# Run with custom parameters
python src/autonomous_trading_crew/ui/cli.py AAPL --output result.json --verbose
```

### Web Interface
```bash
# Start the Streamlit web application
streamlit run src/autonomous_trading_crew/ui/streamlit_app.py
```

### Jupyter Notebook
Open `src/autonomous_trading_crew/examples/interactive_analysis.ipynb` in Jupyter to run interactive analysis.

## Understanding the Analysis Process

### 1. Market Intelligence Analysis
The Market Intelligence Analyst gathers and analyzes:
- Current stock price, volume, and market cap
- Recent news sentiment using FinBERT
- Analyst ratings and price targets
- Technical indicators (RSI, moving averages, etc.)
- Sector and market context

### 2. Risk Assessment
The Risk Management Officer evaluates:
- Trading signal validation
- Volatility assessment (VIX levels, historical volatility)
- Position sizing based on portfolio risk
- Sector concentration risk
- Market conditions and economic indicators
- Stop-loss and take-profit levels

### 3. Execution Planning
The Trade Execution Specialist creates:
- Optimal order strategies (market, limit, stop-limit)
- Execution timing based on volume patterns
- Tax optimization strategies
- Contingency plans for various scenarios
- Monitoring and reporting requirements

### 4. Decision Reporting
The Explainability Reporter generates:
- Executive summary with key recommendations
- Detailed market analysis synthesis
- Risk assessment results
- Execution plan overview
- Clear decision rationale
- Audit trail of the entire process

## Customization

### Agent Configuration
Modify `src/autonomous_trading_crew/config/agents.yaml` to customize agent behavior:
- Roles and goals
- Backstories and expertise
- Tool assignments

### Task Configuration
Modify `src/autonomous_trading_crew/config/tasks.yaml` to customize task behavior:
- Analysis requirements
- Expected output formats
- Validation criteria

## Interpreting Results

### JSON Output Format
The system generates structured JSON output with:
- Market data and technical indicators
- Sentiment analysis results
- Risk metrics and position sizing
- Execution recommendations
- Confidence levels for all decisions

### Report Structure
The final report includes:
- Executive summary with investment recommendation
- Detailed market analysis
- Risk assessment findings
- Execution plan details
- Decision rationale with supporting data
- Key risks and mitigation strategies

## Troubleshooting

### Common Issues

1. **API Key Errors**
   - Verify API keys in `.env` file
   - Check API key validity with providers
   - Ensure internet connectivity

2. **Dependency Issues**
   - Reinstall dependencies: `pip install -r requirements.txt`
   - Check Python version compatibility
   - Install missing packages individually

3. **Performance Issues**
   - Check internet connection speed
   - Reduce data timeframe for analysis
   - Close other resource-intensive applications

4. **Analysis Errors**
   - Verify stock symbol is valid and traded
   - Check for market data availability
   - Ensure sufficient historical data exists

### Error Messages

- **"API key missing"**: Check `.env` file configuration
- **"Stock symbol not found"**: Verify the symbol is correct and traded
- **"Insufficient data"**: Try a different stock with more history
- **"Model loading failed"**: Check internet connection and dependencies

## Best Practices

### For Accurate Analysis
- Use actively traded stocks with sufficient history
- Run analysis during market hours for real-time data
- Review multiple stocks for portfolio diversification
- Consider market conditions and economic events

### For Performance Optimization
- Use the CLI for automated batch processing
- Use the web interface for interactive exploration
- Save results to files for historical comparison
- Monitor API usage to stay within limits

### For Risk Management
- Review risk assessments carefully
- Consider position sizing recommendations
- Monitor stop-loss and take-profit levels
- Diversify investments across multiple stocks

## Advanced Usage

### Custom Tools Development
Add new tools by:
1. Creating a new file in `src/autonomous_trading_crew/tools/`
2. Implementing the tool as a CrewAI BaseTool subclass
3. Adding the tool to the appropriate agent

### New Agent Integration
Add new agents by:
1. Creating a new file in `src/autonomous_trading_crew/agents/`
2. Implementing the agent creation function
3. Adding agent configuration to `config/agents.yaml`
4. Registering the agent in `crew.py`

### Task Extension
Add new tasks by:
1. Creating a new file in `src/autonomous_trading_crew/tasks/`
2. Implementing the task creation function
3. Adding task configuration to `config/tasks.yaml`
4. Registering the task in `crew.py`

## Support and Feedback

For support, questions, or feedback:
- Check the documentation in the `docs/` directory
- Review the implementation summary in `IMPLEMENTATION_SUMMARY.md`
- Submit issues to the project repository
- Contact the development team for enterprise support

## Legal and Compliance

### Disclaimer
This tool is for educational and research purposes only. It does not constitute financial advice. Always do your own research and consult with financial professionals before making investment decisions.

### Data Privacy
- API keys are stored locally in `.env` file
- No personal financial data is stored by the system
- Market data is retrieved from public sources
- Analysis results are stored only locally

### Compliance
- Follow all applicable securities laws and regulations
- Ensure proper licensing for algorithmic trading activities
- Comply with API provider terms of service
- Maintain proper records for regulatory requirements