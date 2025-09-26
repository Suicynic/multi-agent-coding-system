#!/bin/bash
# Setup examples for using the Orchestrator system.
#
# This script provides example commands for different scenarios.
echo "🤖 Orchestrator Multi-Agent Coding System - Usage Examples"
printf '=%.0s' {1..60}; echo

echo "
📋 Basic Usage Examples:

1. Add unit tests to current repository:
   python orchestrator_cli.py \"Add comprehensive unit tests for the core functionality\"

2. Fix a specific bug:
   python orchestrator_cli.py \"Fix the memory leak in the data processing module\" --max-turns 25

3. Add documentation:
   python orchestrator_cli.py \"Add API documentation with examples for all public methods\"

4. Refactor code:
   python orchestrator_cli.py \"Refactor the authentication system to use dependency injection\"

5. Add error handling:
   python orchestrator_cli.py \"Add proper error handling and logging throughout the application\"
"

echo "
🔧 Configuration Examples:

1. Use a different model:
   python orchestrator_cli.py \"Add tests\" --model \"openai/gpt-4\"

2. Use custom temperature:
   python orchestrator_cli.py \"Optimize performance\" --temperature 0.05

3. Work on a different directory:
   python orchestrator_cli.py \"Add validation\" --directory /path/to/project

4. Enable detailed logging:
   python orchestrator_cli.py \"Fix bugs\" --logging-dir ./logs --verbose
"

echo "
🏗️ Framework-Specific Examples:

Python/Django:
   python orchestrator_cli.py \"Add Django REST API endpoints for user management\"
   python orchestrator_cli.py \"Implement proper Django authentication with JWT tokens\"

JavaScript/React:
   python orchestrator_cli.py \"Add React Testing Library tests for all components\"
   python orchestrator_cli.py \"Implement Redux state management for the shopping cart\"

Node.js/Express:
   python orchestrator_cli.py \"Add Express middleware for request validation and logging\"
   python orchestrator_cli.py \"Implement proper error handling in all API endpoints\"

Java/Spring:
   python orchestrator_cli.py \"Add Spring Boot unit tests with proper test coverage\"
   python orchestrator_cli.py \"Implement Spring Security for API authentication\"
"

echo "
📊 Repository Analysis:

1. Analyze current repository:
   python repo_analyzer.py

2. Analyze a different repository:
   python repo_analyzer.py /path/to/project

3. Get quick summary:
   python repo_analyzer.py --summary-only
"

echo "
⚙️ Configuration Management:

1. Create sample configuration file:
   python orchestrator_config.py --create-sample

2. View current configuration:
   python orchestrator_config.py --show
   # or
   python orchestrator_cli.py --show-config

3. Set configuration values:
   python orchestrator_config.py --set model \"openai/gpt-4\"
   python orchestrator_config.py --set temperature 0.2
   python orchestrator_config.py --set max_turns 40
"

echo "
🌍 Environment Setup:

# Set your API key (required)
export LITELLM_API_KEY=\"your-api-key-here\"

# Optional: Set default model
export LITELLM_MODEL=\"anthropic/claude-sonnet-4-20250514\"

# Optional: Set default temperature  
export LITELLM_TEMPERATURE=\"0.1\"

# Optional: Custom API base (for self-hosted or alternative providers)
export LITELLM_API_BASE=\"https://your-api-base.com\"
"

echo "
🎯 Task Examples by Category:

Testing:
- \"Add comprehensive unit tests with at least 80% coverage\"
- \"Create integration tests for the API endpoints\"
- \"Add end-to-end tests using Selenium/Playwright\"

Documentation:
- \"Generate API documentation with OpenAPI/Swagger\"
- \"Add inline documentation and docstrings to all functions\"
- \"Create user guide with code examples\"

Performance:
- \"Optimize database queries and add proper indexing\"
- \"Implement caching to improve response times\"
- \"Add performance monitoring and metrics\"

Security:
- \"Add input validation and sanitization\"
- \"Implement proper authentication and authorization\"
- \"Fix security vulnerabilities identified by audit\"

Code Quality:
- \"Refactor duplicate code and improve maintainability\"
- \"Add linting rules and fix all style issues\"
- \"Implement proper error handling throughout the codebase\"

Features:
- \"Add user registration and email verification\"
- \"Implement file upload with proper validation\"
- \"Add search functionality with filtering and pagination\"
"

echo "
💡 Tips for Better Results:

1. Be specific about what you want:
   ❌ \"Fix bugs\"
   ✅ \"Fix the authentication timeout bug in the login system\"

2. Provide context when needed:
   ✅ \"Add unit tests for the payment processing module using pytest\"

3. Set appropriate turn limits:
   - Simple tasks: 10-20 turns
   - Medium tasks: 20-40 turns
   - Complex tasks: 40-80 turns

4. Use logging for complex tasks:
   python orchestrator_cli.py \"complex task\" --logging-dir ./logs

5. Analyze your repo first:
   python repo_analyzer.py
"

echo "
🚨 Troubleshooting:

1. API Key Issues:
   - Make sure LITELLM_API_KEY is set
   - Check your API key has sufficient credits
   - Verify the model you're using is available

2. Permission Issues:
   - Make sure the orchestrator can read/write files in the target directory
   - Check file permissions if running on files created by other users

3. Model Issues:
   - Try a different model if one isn't working
   - Check LiteLLM documentation for supported models
   - Some models may require different API base URLs

4. Task Completion:
   - Increase max-turns for complex tasks
   - Break down very large tasks into smaller ones
   - Use --verbose to see detailed execution logs
"