# Using Orchestrator on Your Own Repositories

This guide explains how to use the Orchestrator multi-agent coding system on your own repositories, not just for TerminalBench evaluation.

## Quick Start

1. **Set up your API key:**
   ```bash
   export LITELLM_API_KEY="your-api-key-here"
   ```

2. **Run the orchestrator on your repository:**
   ```bash
   python orchestrator_cli.py "Add unit tests for the authentication module"
   ```

That's it! The orchestrator will coordinate explorer and coder agents to complete your task.

## Installation

### Prerequisites
- Python 3.12+ 
- API key for LiteLLM-supported models (Anthropic, OpenAI, etc.)

### Setup
```bash
# Clone the repository
git clone https://github.com/Suicynic/multi-agent-coding-system.git
cd multi-agent-coding-system

# Install dependencies (using pip since uv might not be available)
pip install litellm pyyaml pydantic

# Set your API key
export LITELLM_API_KEY="your-api-key-here"

# Test with a simple task
python orchestrator_cli.py "Create a hello.txt file with 'Hello World'"
```

## CLI Interface

### Basic Usage
```bash
python orchestrator_cli.py "Your task description here"
```

### Common Options
```bash
# Work on a specific directory
python orchestrator_cli.py "Add tests" --directory /path/to/your/project

# Use a different model
python orchestrator_cli.py "Fix bugs" --model "openai/gpt-4"

# Adjust creativity (0.0 = focused, 1.0 = creative)
python orchestrator_cli.py "Refactor code" --temperature 0.2

# Set maximum turns before stopping
python orchestrator_cli.py "Complex task" --max-turns 40

# Enable detailed logging
python orchestrator_cli.py "Debug issue" --logging-dir ./logs --verbose
```

### Configuration Management
```bash
# Create a configuration file with your preferences
python orchestrator_config.py --create-sample

# View current configuration
python orchestrator_cli.py --show-config

# Set default values
python orchestrator_config.py --set model "openai/gpt-4"
python orchestrator_config.py --set temperature 0.1
```

## Repository Analysis

Before using the orchestrator, analyze your repository to understand what it can work with:

```bash
# Analyze current directory
python repo_analyzer.py

# Analyze a specific directory
python repo_analyzer.py /path/to/your/project

# Quick summary
python repo_analyzer.py --summary-only
```

The analyzer will show:
- Programming languages used
- Project structure and frameworks
- Suggested tasks the orchestrator could help with

## Task Examples

### Testing
```bash
python orchestrator_cli.py "Add comprehensive unit tests with at least 80% coverage"
python orchestrator_cli.py "Create integration tests for the API endpoints"
python orchestrator_cli.py "Add end-to-end tests using pytest and Selenium"
```

### Documentation
```bash
python orchestrator_cli.py "Generate API documentation with examples"
python orchestrator_cli.py "Add docstrings to all functions and classes"
python orchestrator_cli.py "Create a comprehensive README with setup instructions"
```

### Bug Fixes
```bash
python orchestrator_cli.py "Fix the memory leak in the data processing module"
python orchestrator_cli.py "Resolve the authentication timeout issue"
python orchestrator_cli.py "Fix all linting errors and warnings"
```

### Feature Development
```bash
python orchestrator_cli.py "Add user registration with email verification"
python orchestrator_cli.py "Implement file upload with validation and security checks"
python orchestrator_cli.py "Add search functionality with filtering and pagination"
```

### Code Quality
```bash
python orchestrator_cli.py "Refactor duplicate code and improve maintainability"
python orchestrator_cli.py "Add proper error handling throughout the application"
python orchestrator_cli.py "Implement logging with appropriate levels and formatting"
```

## Framework-Specific Examples

### Python/Django
```bash
python orchestrator_cli.py "Add Django REST API endpoints for user management"
python orchestrator_cli.py "Implement Django authentication with JWT tokens"  
python orchestrator_cli.py "Add Django admin interface for content management"
```

### JavaScript/React
```bash
python orchestrator_cli.py "Add React Testing Library tests for all components"
python orchestrator_cli.py "Implement Redux state management for the shopping cart"
python orchestrator_cli.py "Add accessibility improvements with ARIA labels"
```

### Node.js/Express
```bash
python orchestrator_cli.py "Add Express middleware for request validation"
python orchestrator_cli.py "Implement proper error handling in all API endpoints"
python orchestrator_cli.py "Add rate limiting and security headers"
```

### Java/Spring
```bash
python orchestrator_cli.py "Add Spring Boot unit tests with proper test coverage"
python orchestrator_cli.py "Implement Spring Security for API authentication"
python orchestrator_cli.py "Add JPA repositories with custom queries"
```

## Programmatic Usage

You can also use the orchestrator programmatically in your own scripts:

```python
from src.agents.orchestrator_agent import OrchestratorAgent
from src.agents.env_interaction.command_executor import LocalExecutor

# Create executor for your repository
executor = LocalExecutor(working_directory="/path/to/your/project")

# Create orchestrator
orchestrator = OrchestratorAgent(
    model="anthropic/claude-sonnet-4-20250514",
    temperature=0.1
)

# Setup and run
orchestrator.setup(executor)
result = orchestrator.run("Add unit tests for the main functionality", max_turns=30)

print(f"Completed: {result['completed']}")
print(f"Message: {result['finish_message']}")
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LITELLM_API_KEY` | API key for LiteLLM (required) | None |
| `LITELLM_MODEL` | Default model to use | `anthropic/claude-sonnet-4-20250514` |
| `LITELLM_TEMPERATURE` | Default temperature | `0.1` |
| `LITELLM_API_BASE` | Custom API base URL | None |

## Supported Models

The orchestrator works with any LiteLLM-supported model:

- **Anthropic**: `anthropic/claude-sonnet-4-20250514`, `anthropic/claude-haiku-3-20240307`
- **OpenAI**: `openai/gpt-4`, `openai/gpt-4-turbo`, `openai/gpt-3.5-turbo`
- **Open Source via OpenRouter**: `openrouter/qwen/qwen3-coder`, `openrouter/deepseek/deepseek-chat-v3.1`
- **And many more**: See [LiteLLM documentation](https://docs.litellm.ai/docs/providers) for the full list

## Tips for Better Results

### 1. Be Specific
❌ **Vague**: "Fix bugs"  
✅ **Specific**: "Fix the authentication timeout bug that occurs after 30 minutes of inactivity"

### 2. Provide Context
❌ **No context**: "Add tests"  
✅ **With context**: "Add pytest unit tests for the payment processing module with mock external API calls"

### 3. Set Appropriate Turn Limits
- **Simple tasks** (file creation, small fixes): 10-20 turns
- **Medium tasks** (adding features, refactoring): 20-40 turns  
- **Complex tasks** (large features, architectural changes): 40-80 turns

### 4. Use Repository Analysis
Run `python repo_analyzer.py` first to understand your codebase and get task suggestions.

### 5. Enable Logging for Complex Tasks
```bash
python orchestrator_cli.py "complex task" --logging-dir ./logs --verbose
```

## How It Works

The Orchestrator uses a multi-agent architecture:

1. **Orchestrator Agent**: Analyzes your task and creates a plan
2. **Explorer Agents**: Read and analyze your codebase (read-only)
3. **Coder Agents**: Implement changes and write code
4. **Context Store**: Shares knowledge between agents to avoid redundant work

The orchestrator never directly touches your code - it delegates all work to specialized agents and coordinates their efforts.

## Limitations

- **Local filesystem only**: Currently works on local repositories (not remote Git repositories)
- **API costs**: Uses external LLM APIs which have costs
- **Turn limits**: Complex tasks may require multiple runs with higher turn limits
- **No rollback**: Changes are made directly to your files (use version control!)

## Troubleshooting

### API Key Issues
```bash
# Make sure your API key is set
echo $LITELLM_API_KEY

# Test with a simple request
python -c "import os; from src.agents.utils.llm_client import get_llm_response; print(get_llm_response([{'role': 'user', 'content': 'Hello'}]))"
```

### Permission Issues
- Ensure the orchestrator can read/write files in your target directory
- Check file permissions if you're working on files created by other users
- Run with appropriate permissions (but avoid running as root unless necessary)

### Model Issues
- Try a different model if one isn't working: `--model "openai/gpt-4"`
- Check that your API key has access to the specified model
- Some models may require different API base URLs

### Task Completion Issues
- Increase `--max-turns` for complex tasks
- Break very large tasks into smaller, more specific ones
- Use `--verbose` to see detailed execution logs
- Check the logs directory if you enabled logging

## Getting Help

- **View examples**: `bash examples/setup_examples.sh`
- **Analyze your repo**: `python repo_analyzer.py`
- **Check configuration**: `python orchestrator_cli.py --show-config`
- **Enable verbose logging**: Add `--verbose` to see detailed execution

## Contributing

This system is designed to be extensible. You can:

- Add new command executors for different environments
- Extend the repository analyzer for new languages/frameworks
- Add new agent types with specialized capabilities
- Improve the context sharing and task management systems

See the main README and PROJECT_STRUCTURE.md for more details on the architecture.