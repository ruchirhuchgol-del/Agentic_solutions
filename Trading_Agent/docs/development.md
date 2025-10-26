# Development Guide

## Getting Started

### Prerequisites
- Python 3.10-3.13
- pip or uv for package management
- API keys for OpenAI and SerperDev

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd autonomous_trading_crew

# Install dependencies
pip install -r requirements.txt

# Or using uv (faster)
uv pip install -r requirements.txt
```

### Environment Setup
Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
# Edit .env to add your API keys
```

## Project Structure

The project follows a modular architecture:

- `src/autonomous_trading_crew/`: Main source code
  - `agents/`: Individual agent implementations
  - `tasks/`: Task definitions and logic
  - `tools/`: Custom financial tools
  - `ui/`: User interfaces (CLI, Streamlit)
  - `utils/`: Utility functions
  - `config/`: YAML configuration files
- `tests/`: Unit and integration tests
- `docs/`: Documentation
- `examples/`: Example usage and notebooks
- `models/`: Trained models (if any)
- `data/`: Data files
- `logs/`: Log files

## Adding New Features

### Adding a New Agent
1. Create a new file in `src/autonomous_trading_crew/agents/`
2. Implement the agent creation function
3. Add the agent configuration to `config/agents.yaml`
4. Import and register the agent in `crew.py`

### Adding a New Task
1. Create a new file in `src/autonomous_trading_crew/tasks/`
2. Implement the task creation function
3. Add the task configuration to `config/tasks.yaml`
4. Import and register the task in `crew.py`

### Adding a New Tool
1. Create a new file in `src/autonomous_trading_crew/tools/`
2. Implement the tool as a CrewAI BaseTool subclass
3. Add the tool to the appropriate agent's tool list
4. Import the tool in the agent file

## Testing

Run tests with:
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_agents.py
```

## Code Style

Follow PEP 8 guidelines:
- Use 4 spaces for indentation
- Limit lines to 88 characters (Black format)
- Use descriptive variable and function names
- Add docstrings to all functions and classes

## Deployment

### Local Development
```bash
# Run the crew
python src/autonomous_trading_crew/main.py run

# Run with specific stock
python src/autonomous_trading_crew/main.py run AAPL

# Run Streamlit interface
streamlit run src/autonomous_trading_crew/ui/streamlit_app.py
```

### Production Deployment
For production deployment, consider:
- Using a virtual environment
- Setting up proper logging
- Configuring environment variables
- Implementing error handling and monitoring

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Run tests to ensure nothing is broken
6. Submit a pull request

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **API Key Issues**: Verify API keys in `.env` file
3. **Network Issues**: Check internet connectivity for API calls
4. **Memory Issues**: Reduce data size or increase system memory

### Debugging Tips

- Use verbose mode to see detailed output
- Check log files in the `logs/` directory
- Use the `test` command to run specific iterations
- Enable debugging in individual tools for detailed insights