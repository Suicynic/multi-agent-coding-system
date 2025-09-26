#!/usr/bin/env python3
"""
Multi-language project example.

This example shows how to use the orchestrator on projects with multiple languages
or when working across different types of codebases.
"""

import sys
from pathlib import Path

# Add parent directory to path to import our orchestrator modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestrator_standalone import StandaloneOrchestrator
from src.agents.env_interaction.command_executor import LocalExecutor
from repo_analyzer import RepoAnalyzer


def analyze_and_suggest_tasks(repo_path: str):
    """Analyze a repository and suggest appropriate tasks."""
    
    analyzer = RepoAnalyzer(Path(repo_path))
    analyzer._scan_files()
    analyzer._analyze_languages()
    
    tasks = []
    
    # Python-specific suggestions
    if 'Python' in analyzer.languages:
        tasks.extend([
            "Add comprehensive pytest unit tests for Python modules with proper mocking",
            "Add type hints to all Python functions using modern syntax",
            "Add Python docstrings following Google or NumPy style guide",
        ])
        
        # Django-specific
        if any('django' in str(f).lower() for files in analyzer.files_by_extension.values() for f in files):
            tasks.append("Add Django REST API endpoints with proper serializers and viewsets")
    
    # JavaScript/TypeScript suggestions
    if any(lang in analyzer.languages for lang in ['JavaScript', 'TypeScript']):
        tasks.extend([
            "Add Jest unit tests for JavaScript/TypeScript functions and components",
            "Add ESLint configuration and fix all linting issues",
            "Implement proper error handling for all async operations",
        ])
        
        # React-specific
        if any('react' in str(f).lower() for files in analyzer.files_by_extension.values() for f in files):
            tasks.append("Add React Testing Library tests for all components")
    
    # Java suggestions
    if 'Java' in analyzer.languages:
        tasks.extend([
            "Add JUnit 5 tests with proper test coverage and assertions",
            "Implement proper exception handling patterns throughout the codebase",
            "Add comprehensive Javadoc documentation for all public methods",
        ])
    
    # Go suggestions
    if 'Go' in analyzer.languages:
        tasks.extend([
            "Add Go unit tests using testify for better assertions and mocking",
            "Implement proper error handling following Go best practices",
            "Add Go benchmark tests for performance-critical functions",
        ])
    
    # Rust suggestions
    if 'Rust' in analyzer.languages:
        tasks.extend([
            "Add comprehensive Rust unit tests with proper error case coverage",
            "Implement proper error handling using Result and Option types",
            "Add documentation examples that are tested with doctests",
        ])
    
    # General suggestions for any codebase
    tasks.extend([
        "Add comprehensive README with setup instructions and usage examples",
        "Implement CI/CD pipeline with automated testing and deployment",
        "Add security audit and fix any identified vulnerabilities",
        "Add performance monitoring and logging throughout the application",
        "Create development environment setup with Docker or similar",
    ])
    
    return tasks, analyzer


def run_multi_language_workflow(repo_path: str):
    """Run a comprehensive workflow for a multi-language project."""
    
    print(f"🔍 Analyzing repository: {repo_path}")
    print("=" * 60)
    
    # Analyze the repository
    tasks, analyzer = analyze_and_suggest_tasks(repo_path)
    
    # Show analysis results
    print("📊 Repository Analysis:")
    print(f"  Total files: {analyzer.total_files}")
    print(f"  Programming languages:")
    for lang, lines in analyzer.languages.most_common(5):
        percentage = (lines / sum(analyzer.languages.values())) * 100
        print(f"    • {lang}: {lines:,} lines ({percentage:.1f}%)")
    
    complexity, desc = analyzer.get_complexity_score()
    print(f"  Complexity: {complexity} ({desc})")
    
    print(f"\n💡 Suggested Tasks ({len(tasks)} total):")
    for i, task in enumerate(tasks[:8], 1):
        print(f"  {i}. {task}")
    if len(tasks) > 8:
        print(f"     ... and {len(tasks) - 8} more")
    
    # Create orchestrator
    executor = LocalExecutor(working_directory=repo_path)
    orchestrator = StandaloneOrchestrator(
        model="anthropic/claude-sonnet-4-20250514",
        temperature=0.1
    )
    orchestrator.setup(executor)
    
    # Example: Run the first suggested task
    if tasks:
        selected_task = tasks[0]
        print(f"\n🚀 Running selected task:")
        print(f"📋 {selected_task}")
        print("-" * 60)
        
        # Uncomment to actually run (requires API key)
        # result = orchestrator.run(selected_task, max_turns=30)
        # print(f"✅ Task completed: {result['completed']}")
        # print(f"📝 Result: {result['finish_message']}")
        
        print("💡 To run this task, use:")
        print(f"python orchestrator_cli.py \"{selected_task}\" --directory \"{repo_path}\"")


def example_cross_platform_tasks():
    """Tasks that work well across different platforms and languages."""
    
    return [
        # Documentation tasks
        "Create comprehensive API documentation with examples and usage patterns",
        "Add inline code documentation following language-specific conventions",
        "Generate project documentation website with proper navigation and search",
        
        # Testing tasks
        "Add comprehensive test suite with unit, integration, and end-to-end tests",
        "Implement test data factories and fixtures for consistent testing",
        "Add performance and load testing for critical application paths",
        
        # CI/CD tasks
        "Set up GitHub Actions workflow with testing, linting, and deployment stages",
        "Add Docker containerization with multi-stage builds for production",
        "Implement automated dependency updates and security scanning",
        
        # Security tasks
        "Perform security audit and implement recommended fixes",
        "Add input validation and sanitization for all user-facing inputs",
        "Implement proper authentication and authorization mechanisms",
        
        # Performance tasks
        "Add performance monitoring and alerting for production systems",
        "Implement caching strategies for frequently accessed data",
        "Optimize database queries and add proper indexing",
        
        # Code quality tasks
        "Set up code formatting and linting with automatic fixes",
        "Refactor duplicate code and improve overall maintainability",
        "Add error handling and logging throughout the application",
        
        # Infrastructure tasks
        "Create production deployment configuration with proper scaling",
        "Add monitoring and observability with metrics and dashboards",
        "Implement backup and disaster recovery procedures",
    ]


def main():
    """Main example runner."""
    print("🌍 Multi-Language Project Examples for Orchestrator")
    print("=" * 65)
    
    print("This example shows how to:")
    print("• Analyze repositories with mixed languages")
    print("• Get language-specific task suggestions")
    print("• Run workflows across different codebases")
    
    # Show cross-platform tasks
    cross_platform_tasks = example_cross_platform_tasks()
    print(f"\n🔧 Cross-Platform Tasks ({len(cross_platform_tasks)} examples):")
    for i, task in enumerate(cross_platform_tasks[:6], 1):
        print(f"  {i}. {task}")
    print(f"     ... and {len(cross_platform_tasks) - 6} more")
    
    print(f"\n📋 Example Usage:")
    print("# Analyze any repository")
    print("python repo_analyzer.py /path/to/project")
    print()
    print("# Run language-agnostic task")
    print("python orchestrator_cli.py \"Add comprehensive documentation with examples\"")
    print()
    print("# Run this multi-language workflow")
    print("python examples/multi_language_example.py")
    
    print(f"\n🎯 Best Practices for Multi-Language Projects:")
    print("• Use the repo analyzer first to understand the codebase")
    print("• Choose tasks appropriate for the dominant language")
    print("• Start with documentation and testing tasks")
    print("• Use specific framework names when known")
    print("• Consider the project's complexity when setting max-turns")
    
    # Run the workflow on current directory as example
    print(f"\n" + "=" * 65)
    run_multi_language_workflow(".")


if __name__ == "__main__":
    main()