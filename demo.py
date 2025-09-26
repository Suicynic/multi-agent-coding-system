#!/usr/bin/env python3
"""
Demo script showing the complete Orchestrator workflow.

This script demonstrates the full capability of the orchestrator system
on different types of repositories and tasks.
"""

import sys
import tempfile
import shutil
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from repo_analyzer import RepoAnalyzer
from orchestrator_config import OrchestratorConfig


def create_demo_python_project():
    """Create a demo Python project for demonstration."""
    
    temp_dir = Path(tempfile.mkdtemp())
    
    # Create a simple Python web API project structure
    (temp_dir / "app").mkdir()
    (temp_dir / "tests").mkdir()
    
    # Main application file
    (temp_dir / "app" / "__init__.py").write_text("")
    (temp_dir / "app" / "main.py").write_text('''
"""Main FastAPI application."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="User Management API")

# In-memory storage (replace with database in production)
users_db = {}
next_user_id = 1

class User(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    age: int

class UserResponse(User):
    id: int

@app.get("/")
def read_root():
    return {"message": "Welcome to User Management API"}

@app.post("/users/", response_model=UserResponse)
def create_user(user: User):
    global next_user_id
    user.id = next_user_id
    users_db[next_user_id] = user
    next_user_id += 1
    return user

@app.get("/users/", response_model=List[UserResponse])
def list_users():
    return list(users_db.values())

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
    return {"message": "User deleted successfully"}
''')
    
    # Utils module
    (temp_dir / "app" / "utils.py").write_text('''
"""Utility functions."""

import re
from typing import Optional

def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def calculate_age_group(age: int) -> str:
    """Calculate age group for demographics."""
    if age < 18:
        return "minor"
    elif age < 65:
        return "adult"
    else:
        return "senior"

def format_user_display_name(name: str) -> str:
    """Format user name for display."""
    return name.title().strip()
''')
    
    # Basic test file
    (temp_dir / "tests" / "__init__.py").write_text("")
    (temp_dir / "tests" / "test_main.py").write_text('''
"""Basic tests for main module."""

def test_placeholder():
    """Placeholder test - needs implementation."""
    assert True
''')
    
    # Requirements file
    (temp_dir / "requirements.txt").write_text('''
fastapi>=0.68.0
uvicorn>=0.15.0
pydantic>=1.8.0
pytest>=6.0.0
httpx>=0.24.0
''')
    
    # Basic README
    (temp_dir / "README.md").write_text('''
# User Management API

A simple FastAPI application for managing users.

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the server: `uvicorn app.main:app --reload`
3. Visit http://localhost:8000/docs for API documentation

## Features

- Create, read, update, delete users
- Email validation
- Age group calculation
- RESTful API design

## TODO

- Add comprehensive tests
- Add database integration
- Add authentication
- Add input validation
- Add error handling
- Add logging
''')
    
    return temp_dir


def demo_repository_analysis():
    """Demonstrate repository analysis capabilities."""
    
    print("🔍 Repository Analysis Demo")
    print("=" * 50)
    
    # Create demo project
    demo_project = create_demo_python_project()
    
    try:
        print(f"📁 Created demo project at: {demo_project}")
        
        # Analyze the repository
        analyzer = RepoAnalyzer(demo_project)
        analyzer.analyze()
        
    finally:
        # Clean up
        shutil.rmtree(demo_project)
        print(f"🧹 Cleaned up demo project")


def demo_configuration_system():
    """Demonstrate configuration management."""
    
    print("\n⚙️  Configuration System Demo")
    print("=" * 50)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        config_file = Path(temp_dir) / "demo_config.json"
        
        # Create and configure
        config = OrchestratorConfig(config_file)
        
        print("📋 Default configuration:")
        config.show_config()
        
        # Modify settings
        config.set("model", "openai/gpt-4")
        config.set("temperature", 0.2)
        config.set("max_turns", 40)
        config.save()
        
        print(f"\n✅ Updated configuration saved to {config_file}")
        
        # Load in new instance to verify persistence
        config2 = OrchestratorConfig(config_file)
        assert config2.get("model") == "openai/gpt-4"
        assert config2.get("temperature") == 0.2
        
        print("✅ Configuration persistence verified")


def demo_task_suggestions():
    """Demonstrate task suggestions for different project types."""
    
    print("\n💡 Task Suggestions Demo")
    print("=" * 50)
    
    project_types = {
        "Python FastAPI Project": [
            "Add comprehensive pytest tests for all API endpoints with proper mocking",
            "Add input validation using Pydantic models with custom validators",
            "Implement async database operations using SQLAlchemy and asyncpg",
            "Add authentication middleware with JWT tokens and refresh tokens",
            "Add comprehensive logging with structured logging and request tracing"
        ],
        "React TypeScript Project": [
            "Add React Testing Library tests for all components with user interaction testing",
            "Implement Redux Toolkit for state management with proper TypeScript types",
            "Add Storybook for component documentation and visual testing",
            "Implement error boundaries for better error handling and user experience",
            "Add accessibility improvements with proper ARIA labels and keyboard navigation"
        ],
        "Java Spring Boot Project": [
            "Add JUnit 5 tests with TestContainers for integration testing",
            "Implement Spring Security with OAuth2 and JWT authentication",
            "Add Spring Data JPA repositories with custom queries and specifications",
            "Implement proper exception handling with @ControllerAdvice",
            "Add comprehensive API documentation using SpringDoc OpenAPI"
        ]
    }
    
    for project_type, tasks in project_types.items():
        print(f"\n🏗️  {project_type}:")
        for i, task in enumerate(tasks, 1):
            print(f"  {i}. {task}")


def demo_cli_commands():
    """Show example CLI commands for different scenarios."""
    
    print("\n🚀 CLI Commands Demo")
    print("=" * 50)
    
    commands = [
        ("Basic usage", 'python3 orchestrator_cli.py "Add unit tests for the user management module"'),
        ("Different directory", 'python3 orchestrator_cli.py "Fix authentication bugs" --directory /path/to/project'),
        ("Different model", 'python3 orchestrator_cli.py "Add documentation" --model "openai/gpt-4"'),
        ("Custom settings", 'python3 orchestrator_cli.py "Refactor database code" --temperature 0.05 --max-turns 40'),
        ("With logging", 'python3 orchestrator_cli.py "Add error handling" --logging-dir ./logs --verbose'),
        ("Repository analysis", 'python3 repo_analyzer.py /path/to/project'),
        ("Configuration", 'python3 orchestrator_config.py --show'),
    ]
    
    for description, command in commands:
        print(f"\n{description}:")
        print(f"  {command}")


def main():
    """Run the complete demo."""
    
    print("🤖 Orchestrator Multi-Agent Coding System Demo")
    print("=" * 60)
    print("This demo shows how to use the orchestrator on your own repositories.")
    
    try:
        # Demo 1: Repository Analysis
        demo_repository_analysis()
        
        # Demo 2: Configuration System
        demo_configuration_system()
        
        # Demo 3: Task Suggestions
        demo_task_suggestions()
        
        # Demo 4: CLI Commands
        demo_cli_commands()
        
        print("\n" + "=" * 60)
        print("✅ Demo completed successfully!")
        
        print("\n🎯 Next Steps:")
        print("1. Set your API key: export LITELLM_API_KEY='your-key'")
        print("2. Analyze your repository: python3 repo_analyzer.py")
        print("3. Run a task: python3 orchestrator_cli.py 'your task'")
        print("4. Read USAGE.md for detailed instructions")
        
        print("\n📚 Resources:")
        print("• USAGE.md - Comprehensive usage guide")
        print("• examples/ - Language-specific examples")
        print("• orchestrator_cli.py --help - Command line help")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())