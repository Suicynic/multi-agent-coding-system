#!/usr/bin/env python3
"""
Basic usage example for the Orchestrator system.

This example shows how to use the Orchestrator programmatically 
(without the CLI) to work on a repository.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.agents.env_interaction.command_executor import LocalExecutor
from orchestrator_standalone import StandaloneOrchestrator


def run_orchestrator_on_repo(repo_path: str, task: str, model: str = "anthropic/claude-sonnet-4-20250514"):
    """
    Run the orchestrator on a specific repository with a given task.
    
    Args:
        repo_path: Path to the repository to work on
        task: Description of the task to complete
        model: LiteLLM model to use
        
    Returns:
        Dictionary with execution results
    """
    # Create local executor for the repository
    executor = LocalExecutor(working_directory=repo_path)
    
    # Create orchestrator
    orchestrator = StandaloneOrchestrator(
        model=model,
        temperature=0.1
    )
    
    # Setup orchestrator
    orchestrator.setup(executor)
    
    print(f"🚀 Running orchestrator on {repo_path}")
    print(f"📋 Task: {task}")
    print(f"🤖 Model: {model}")
    print("-" * 50)
    
    # Execute the task
    result = orchestrator.run(task, max_turns=30)
    
    return result


def main():
    """Example usage."""
    # Example 1: Add tests to current directory
    result1 = run_orchestrator_on_repo(
        repo_path=".",
        task="Add unit tests for the main functionality"
    )
    
    print("Result 1:", result1)
    
    # Example 2: Fix a bug in a specific directory
    # result2 = run_orchestrator_on_repo(
    #     repo_path="/path/to/my/project",
    #     task="Fix the authentication bug in the login system",
    #     model="openai/gpt-4"
    # )
    
    # Example 3: Add documentation
    # result3 = run_orchestrator_on_repo(
    #     repo_path="/path/to/my/project", 
    #     task="Add comprehensive API documentation with examples"
    # )


if __name__ == "__main__":
    main()