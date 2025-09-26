#!/usr/bin/env python3
"""
Example usage for Python projects.

This example shows specific tasks that work well with Python codebases.
"""

import sys
from pathlib import Path

# Add parent directory to path to import our orchestrator modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestrator_standalone import StandaloneOrchestrator
from src.agents.env_interaction.command_executor import LocalExecutor


def example_python_tasks():
    """Example tasks specifically useful for Python projects."""
    
    python_tasks = [
        # Testing tasks
        "Add comprehensive pytest unit tests for all functions in the core module with at least 80% coverage",
        "Create integration tests for the API endpoints using pytest and mock external dependencies",
        "Add property-based tests using Hypothesis for data validation functions",
        
        # Code quality tasks
        "Add type hints to all functions and classes using Python 3.9+ syntax",
        "Add comprehensive docstrings following Google style to all public functions and classes",
        "Refactor large functions to be smaller and more maintainable, following single responsibility principle",
        
        # Django-specific tasks
        "Add Django REST framework serializers and viewsets for the User model with proper validation",
        "Implement Django authentication with JWT tokens and refresh token rotation",
        "Add Django admin interface with proper list display, filters, and search functionality",
        "Create Django management commands for data migration and cleanup tasks",
        
        # Flask-specific tasks
        "Add Flask-RESTful API endpoints with proper error handling and validation using marshmallow",
        "Implement Flask authentication using Flask-Login and bcrypt for password hashing",
        "Add Flask application factory pattern with proper configuration management",
        
        # FastAPI-specific tasks
        "Add FastAPI endpoints with proper Pydantic models and automatic OpenAPI documentation",
        "Implement FastAPI authentication with OAuth2 and JWT tokens",
        "Add FastAPI middleware for request logging and CORS handling",
        
        # Performance and monitoring
        "Add logging configuration with proper log levels and structured logging using structlog",
        "Implement caching using Redis for expensive database queries and API calls",
        "Add performance monitoring with custom metrics and timing decorators",
        
        # DevOps and deployment
        "Create Dockerfile with multi-stage build for production deployment",
        "Add GitHub Actions workflow for testing, linting, and deployment",
        "Create requirements.txt and setup.py with proper dependency management",
        
        # Security tasks
        "Add input validation and sanitization for all user inputs using marshmallow or Pydantic",
        "Implement rate limiting for API endpoints using Flask-Limiter or similar",
        "Add security headers middleware and CSRF protection",
        
        # Database tasks
        "Add SQLAlchemy models with proper relationships and constraints",
        "Create Alembic database migrations for schema changes",
        "Add database connection pooling and transaction management",
    ]
    
    return python_tasks


def run_python_task_example(repo_path: str = "."):
    """Run an example Python task."""
    
    # Create executor for the repository
    executor = LocalExecutor(working_directory=repo_path)
    
    # Create orchestrator
    orchestrator = StandaloneOrchestrator(
        model="anthropic/claude-sonnet-4-20250514",
        temperature=0.1
    )
    
    # Setup orchestrator
    orchestrator.setup(executor)
    
    # Example task: Add comprehensive testing
    task = "Add pytest unit tests for all functions in the main module with proper mocking and at least 80% test coverage"
    
    print(f"🐍 Running Python-specific task on {repo_path}")
    print(f"📋 Task: {task}")
    print("-" * 80)
    
    # Execute the task
    result = orchestrator.run(task, max_turns=30)
    
    print(f"\n📊 Results:")
    print(f"Completed: {result['completed']}")
    print(f"Message: {result['finish_message']}")
    print(f"Turns: {result['turns_executed']}")
    
    return result


def main():
    """Main example runner."""
    print("🐍 Python Project Examples for Orchestrator")
    print("=" * 60)
    
    tasks = example_python_tasks()
    
    print(f"\n📋 {len(tasks)} Example Python Tasks:")
    for i, task in enumerate(tasks[:10], 1):  # Show first 10
        print(f"{i:2}. {task}")
    
    if len(tasks) > 10:
        print(f"    ... and {len(tasks) - 10} more!")
    
    print(f"\n🚀 Example Usage:")
    print(f"python orchestrator_cli.py \"{tasks[0]}\"")
    
    print(f"\n💡 Tips for Python Projects:")
    print("• Use specific testing frameworks: 'Add pytest tests' vs 'Add unit tests'")
    print("• Mention Python versions: 'Add type hints using Python 3.10+ syntax'")
    print("• Specify frameworks: 'Add FastAPI endpoints' vs 'Add API endpoints'")
    print("• Include code quality tools: 'Add black formatting and flake8 linting'")
    
    # Uncomment to run an actual example (requires API key)
    # run_python_task_example(".")


if __name__ == "__main__":
    main()