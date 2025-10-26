# GitHub Profile Optimizer

An enterprise-grade, AI-powered GitHub profile optimization tool that analyzes your GitHub presence and provides actionable recommendations to improve your recruiter visibility and professional branding.

## Enterprise Features

- Advanced Caching Layer: Multi-tier caching (memory, Redis, disk) to reduce API calls and improve performance
- Intelligent Rate Limiting: Adaptive throttling to respect GitHub API limits across distributed systems
- Multi-Tenancy Architecture: Isolated tenant environments for enterprise adoption
- Predictive Optimization Engine: ML-powered recommendations for proactive profile improvements
- Microservices Architecture: Scalable, distributed system design with API gateway
- Disaster Recovery & High Availability: Multi-region deployment with automatic failover
- Comprehensive Observability: Structured logging, metrics, and health checks

## Quick Start

### Prerequisites

- Python 3.10 or higher
- GitHub Personal Access Token (with repo scope)
- OpenAI API Key
- Docker (optional, for containerized deployment)
- Redis (optional, for caching and rate limiting)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/github-profile-optimizer.git
cd github-profile-optimizer

# Install dependencies
pip install -e .

# For development
pip install -e ".[dev]"
```

### Basic Usage

Optimize your GitHub profile with a single command:

```bash
python -m src.github_profile_optimizer.main run \
  --github_handle your_username \
  --target_roles "Software Engineer" \
  --dry_run
```

### Docker Deployment (Monolithic)

```bash
# Build the Docker image
docker build -t github-optimizer .

# Run the container
docker run -e GITHUB_TOKEN=your_token \
           -e OPENAI_API_KEY=your_key \
           -p 8000:8000 \
           github-optimizer
```

### Docker Compose (Microservices)

```bash
# Copy and configure environment variables
cp .env.example .env
# Edit .env to add your tokens

# Start microservices
docker-compose -f infrastructure/docker-compose.microservices.yml up
```

### Kubernetes Deployment

```bash
# Deploy to Kubernetes
kubectl apply -f infrastructure/k8s/github-optimizer.yaml
```

## Machine Learning Capabilities

The GitHub Profile Optimizer includes ML-powered predictive capabilities to provide intelligent recommendations. The system can operate in two modes:

1. **Rules-based approach** (default): Uses heuristic rules to generate recommendations
2. **ML-based approach**: Uses trained models for more accurate predictions

### Training ML Models with Jupyter Notebook

The project includes a comprehensive Jupyter notebook for training ML models:

```bash
# Start Jupyter notebook
jupyter notebook GitHub_Profile_Optimizer_Model_Training.ipynb
```

The notebook provides:
- Interactive model training with synthetic data generation
- Hyperparameter tuning capabilities
- Model evaluation and visualization
- Automatic model saving and metadata generation

### Training ML Models with Script

Alternatively, you can train models using the command-line script:

```bash
# Generate synthetic training data and train models
python scripts/train_model.py --samples 2000 --tune --model-type random_forest

# For faster training without hyperparameter tuning
python scripts/train_model.py --samples 1000 --no-tune --model-type gradient_boost
```

This will generate:
- Trained model files in the `models/` directory
- Training logs in `training.log`
- Metadata files with model specifications

### Using Trained Models

Once you have trained models, the predictive optimizer will automatically use them:

```python
from src.github_profile_optimizer.ml.predictive_optimizer import predictive_optimizer

# The optimizer will automatically load the most recent trained model
# if one exists in the models directory
recommendations = predictive_optimizer.suggest_improvements(profile, repositories)
```

### Model Features

The ML models use the following features for predictions:
- Profile completeness metrics
- Repository statistics (count, stars, languages)
- Activity patterns
- Description quality
- Follower/following ratios

The models predict:
- Need for bio improvement
- Repository description requirements
- Activity boost suggestions
- Language showcase opportunities
- Repository pinning recommendations
- Impact scores for each recommendation

## Advanced Caching Layer

The system implements a three-layer caching strategy to minimize GitHub API calls:

1. L1 Cache (Memory): 1-hour TTL for frequently accessed data
2. L2 Cache (Redis): 24-hour TTL for shared cache across instances
3. L3 Cache (Disk): 7-day TTL for long-term storage

```python
from src.github_profile_optimizer.utils.cache_manager import cache_manager

# Cache any data
cache_manager.set("key", {"data": "value"})
cached_data = cache_manager.get("key")
```

### Intelligent Rate Limiting

Adaptive rate limiting prevents exceeding GitHub API quotas:

```python
from src.github_profile_optimizer.utils.rate_limiter import rate_limiter

# Check if API call is allowed
try:
    rate_limiter.api_call("/users/username")
    # Make API call
except RateLimitExceeded:
    # Handle rate limit exceeded
    pass
```

### Multi-Tenancy Architecture

Enterprise-grade tenant isolation for multiple organizations:

```python
from src.github_profile_optimizer.auth.tenant_manager import tenant_manager

# Add tenant
tenant_manager.add_tenant("acme-corp", {
    "github_token": "ghp_...",
    "rate_limit": 1000,
    "allowed_roles": ["Engineer", "Manager"]
})

# Get tenant client
client = tenant_manager.get_client("acme-corp")
```

### Predictive Optimization Engine

ML-powered recommendations for proactive profile improvements:

```python
from src.github_profile_optimizer.ml.predictive_optimizer import predictive_optimizer

# Get predictive recommendations
recommendations = predictive_optimizer.suggest_improvements(profile, repositories)
```

### Microservices Architecture

Scalable service decomposition:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  API Gateway    │    │  Profile Service│    │  Repo Service   │
│  (Flask)        │◄──►│  (Flask)        │◄──►│  (Flask)        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Content Service│    │  CI Service     │    │  Analytics Svc  │
│  (Flask)        │    │  (Flask)        │    │  (Flask)        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Disaster Recovery & High Availability

Multi-region deployment with automatic failover:

```
Region 1 (US-East)          Region 2 (EU-West)
┌─────────────┐            ┌─────────────┐
│  Primary DB │◄─Replication─►│  Standby DB │
│  (Postgres) │            │  (Postgres) │
└─────────────┘            └─────────────┘
       │                          │
       ▼                          ▼
┌─────────────┐            ┌─────────────┐
│  Active K8s │            │  Passive K8s│
│  Cluster    │            │  Cluster    │
└─────────────┘            └─────────────┘
```

## Documentation

### Configuration

The tool uses YAML configuration files for agents and tasks:

- src/github_profile_optimizer/config/agents.yaml: Defines agent roles and capabilities
- src/github_profile_optimizer/config/tasks.yaml: Specifies task parameters and expected outputs

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| github_handle | GitHub username to optimize | Required |
| target_roles | Target job roles | "Software Engineer" |
| repos_scope | Repository scope (public/private/all) | "public" |
| dry_run | Preview changes without applying | True |
| limits | Optimization level (minimal/moderate/comprehensive) | "minimal" |

### API Endpoints

When running the API server, the following endpoints are available:

- GET /health: Health check endpoint
- POST /optimize: Optimize a GitHub profile
- POST /analyze: Analyze a GitHub profile

Example API request:

```bash
curl -X POST http://localhost:8000/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "github_handle": "your_username",
    "target_roles": "Software Engineer",
    "dry_run": true
  }'
```

### Output Schema

The tool generates a comprehensive JSON report with the following sections:

```json
{
  "signal_model": {
    "weights": {
      "stars_growth": 0.2,
      "contribution_cadence": 0.2,
      "topical_alignment": 0.2,
      "readme_clarity": 0.2,
      "repo_health": 0.2
    },
    "rationale": "Balanced scoring across key recruiter signals"
  },
  "current_audit": { ... },
  "recommendations": [ ... ],
  "actions_plan": { ... },
  "pinned_plan": { ... },
  "readme_drafts": { ... },
  "ci_setup": { ... },
  "contribution_coaching": { ... },
  "dynamic_content": { ... },
  "storytelling": { ... },
  "benchmarking": { ... },
  "safety_log": { ... }
}
```

## Development

### Setting Up Development Environment

1. Clone and install dependencies
   ```bash
   git clone https://github.com/yourusername/github-profile-optimizer.git
   cd github-profile-optimizer
   pip install -e ".[dev]"
   pre-commit install
   ```

2. Run tests
   ```bash
   pytest
   ```

3. Run linting
   ```bash
   flake8 src/
   mypy src/
   ```

### Project Structure

```
github-profile-optimizer/
├── src/github_profile_optimizer/
│   ├── agents/                 # Agent definitions
│   ├── api/                    # API gateway and services
│   ├── auth/                   # Authentication and tenant management
│   ├── config/                 # YAML configuration files
│   ├── ml/                     # Machine learning models
│   ├── models/                 # Data models
│   ├── services/               # Business logic services
│   ├── tools/                  # Custom tools (GitHub, File)
│   ├── ui/                     # Dashboard and user interface
│   ├── utils/                  # Utilities (validators, logging, caching)
│   ├── exceptions.py           # Custom exceptions
│   ├── metrics.py              # Metrics collection
│   ├── health.py               # Health checks
│   ├── crew.py                 # Crew orchestration
│   └── main.py                 # CLI entry point
├── tests/                      # Test suite
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
│   ├── fixtures/               # Test fixtures
│   └── conftest.py             # pytest configuration
├── infrastructure/
│   ├── docker-compose.yml      # Local dev stack (monolithic)
│   ├── docker-compose.microservices.yml # Microservices stack
│   ├── k8s/                    # Kubernetes manifests
│   ├── dr/                     # Disaster recovery configurations
│   ├── monitoring/             # Prometheus/Grafana configs
│   └── ci-cd/                  # GitHub Actions workflows
├── docs/
│   ├── api/                    # API documentation
│   └── architecture/           # Architecture documentation
├── .github/workflows/          # CI/CD pipelines
├── scripts/                    # Utility scripts
├── .env.example               # Environment template
├── .pre-commit-config.yaml    # Pre-commit hooks
├── Dockerfile                 # Container configuration
├── requirements-dev.txt       # Development dependencies
└── README.md                  # This file
```

### Architecture Overview

The system follows a multi-agent architecture using crewAI with enterprise enhancements:

1. GitHub Automation Agent: Analyzes GitHub profiles and repositories
2. Profile Analyst Agent: Deep analysis of profile strengths and weaknesses
3. Optimization Specialist Agent: Generates targeted recommendations
4. File Operations Tool: Safely manages file modifications
5. Task Orchestration: Coordinates agent workflows with error handling
6. Validation Layer: Ensures input integrity and safe operations
7. State Management: Tracks operation progress with Redis
8. Observability: Structured logging and metrics collection
9. Caching Layer: Multi-tier caching for performance
10. Rate Limiting: Intelligent API throttling
11. Multi-Tenancy: Tenant isolation for enterprise use
12. ML Engine: Predictive optimization recommendations

## Testing

Run the full test suite:
```bash
pytest --cov=src/github_profile_optimizer --cov-report=html
```

Run specific test categories:
```bash
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m slow          # Include slow tests
```

Test enterprise features:
```bash
python scripts/test-enterprise-features.py
```

Test ML capabilities:
```bash
python scripts/test_ml_optimizer.py
```

Test dashboard components:
```bash
python scripts/test_dashboard.py
```

Train ML models with notebook:
```bash
jupyter notebook GitHub_Profile_Optimizer_Model_Training.ipynb
```

Train ML models with script:
```bash
python scripts/train_model.py --samples 1000
```

## Enterprise GitHub Profile Optimizer Dashboard

The project includes a comprehensive Streamlit dashboard for visualizing and managing GitHub profile optimizations:

```bash
# Start the dashboard using the CLI entry point
dashboard

# Or directly with Streamlit
streamlit run src/github_profile_optimizer/ui/dashboard.py
```

The dashboard provides:
- Interactive profile analysis and optimization
- Real-time caching and ML model status monitoring
- Multi-tenancy support with isolated tenant configurations
- Comprehensive visualization of optimization results
- Detailed recommendations with impact/effort analysis
- Action plan execution with dry-run capabilities

### Features

- **Multi-Tier Caching Visualization**: Real-time monitoring of L1/L2/L3 cache performance
- **ML Model Status**: View model loading status, accuracy metrics, and feature importance
- **Profile Audit Dashboard**: Comprehensive analysis of profile completeness and discoverability
- **Recommendation Engine**: AI-powered recommendations with visual impact/effort matrix
- **Action Plan Execution**: Execute optimization actions with safety checks and dry-run mode
- **Multi-Tenancy Support**: Isolated environments for different organizations or users

### Development Workflow

1. Fork the repository
2. Create a feature branch (git checkout -b feature/amazing-feature)
3. Commit your changes (git commit -m 'Add amazing feature')
4. Push to the branch (git push origin feature/amazing-feature)
5. Open a Pull Request

### Code Style

- Follow PEP 8 style guidelines
- Use type hints for all functions
- Write docstrings for all public methods
- Ensure all tests pass before submitting

## Monitoring & Logging

The application provides comprehensive logging:

- Application Logs: Structured JSON format for easy parsing
- Metrics Collection: Execution times, success rates, etc.
- Health Checks: Endpoint for monitoring service status
- Error Tracking: Detailed error reporting with stack traces

For production deployments, consider integrating with:

- Prometheus/Grafana: Metrics collection and visualization
- ELK Stack: Log aggregation and analysis
- Sentry: Error tracking and alerting

## Security

- Token Management: All API keys stored in environment variables
- Path Validation: Prevents directory traversal attacks
- Rate Limiting: Respects GitHub API rate limits
- Dry Run Mode: Safe preview of changes before application
- Input Sanitization: Protection against injection attacks
- Tenant Isolation: Secure multi-tenant architecture

## Performance

- Concurrent Processing: Efficient task execution with crewAI
- Caching: Multi-tier caching reduces redundant API calls
- Batch Operations: Optimized file operations
- Resource Limits: Configurable constraints to prevent abuse
- Rate Limiting: Intelligent throttling for optimal API usage

## Troubleshooting

### Common Issues

1. GitHub API Rate Limiting
   - Solution: Wait for rate limit reset or use authentication
   - Check: curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/rate_limit

2. File Permission Errors
   - Solution: Ensure write permissions in target directories
   - Check: ls -la on target directory

3. Invalid GitHub Token
   - Solution: Verify token has repo scope
   - Regenerate token at GitHub Settings > Developer settings

4. Redis Connection Issues
   - Solution: Ensure Redis is running and accessible
   - Check: redis-cli ping should return "PONG"

5. Tenant Configuration Issues
   - Solution: Verify tenant configuration in environment variables
   - Check: TENANT_*_CONFIG environment variables

## Acknowledgments

- crewAI for the multi-agent framework
- GitHub API for comprehensive developer platform
- OpenAI for powerful language models
- Pydantic for data validation
- Flask for web API framework
- Redis for caching and state management

## Support

Email: ruchirhuchgol@gmail.com