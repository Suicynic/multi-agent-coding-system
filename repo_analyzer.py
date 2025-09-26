#!/usr/bin/env python3
"""
Repository Analyzer for the Orchestrator system.

This utility analyzes a repository to help users understand:
- What programming languages are used
- Project structure and complexity
- What kinds of tasks the orchestrator could help with
"""

import argparse
import os
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Tuple
import re


class RepoAnalyzer:
    """Analyzes a repository to understand its structure and suggest tasks."""
    
    LANGUAGE_EXTENSIONS = {
        '.py': 'Python',
        '.js': 'JavaScript', 
        '.ts': 'TypeScript',
        '.jsx': 'React/JavaScript',
        '.tsx': 'React/TypeScript',
        '.java': 'Java',
        '.cpp': 'C++',
        '.cc': 'C++',
        '.cxx': 'C++',
        '.c': 'C',
        '.h': 'C/C++ Header',
        '.hpp': 'C++ Header',
        '.go': 'Go',
        '.rs': 'Rust',
        '.rb': 'Ruby',
        '.php': 'PHP',
        '.cs': 'C#',
        '.swift': 'Swift',
        '.kt': 'Kotlin',
        '.scala': 'Scala',
        '.sh': 'Shell Script',
        '.bash': 'Bash Script',
        '.zsh': 'Zsh Script',
        '.yml': 'YAML',
        '.yaml': 'YAML',
        '.json': 'JSON',
        '.xml': 'XML',
        '.html': 'HTML',
        '.css': 'CSS',
        '.scss': 'SCSS',
        '.sass': 'Sass',
        '.sql': 'SQL',
        '.md': 'Markdown',
        '.rst': 'reStructuredText',
        '.dockerfile': 'Docker',
        '.tf': 'Terraform',
        '.vue': 'Vue.js',
        '.svelte': 'Svelte'
    }
    
    BUILD_FILES = {
        'package.json': 'Node.js/npm project',
        'yarn.lock': 'Yarn project',
        'requirements.txt': 'Python pip requirements',
        'pyproject.toml': 'Python poetry/modern project',
        'setup.py': 'Python setuptools project',
        'Pipfile': 'Python pipenv project',
        'poetry.lock': 'Python poetry project',
        'Cargo.toml': 'Rust project',
        'go.mod': 'Go module',
        'pom.xml': 'Maven Java project',
        'build.gradle': 'Gradle project',
        'CMakeLists.txt': 'CMake C/C++ project',
        'Makefile': 'Make-based project',
        'composer.json': 'PHP Composer project',
        'Gemfile': 'Ruby Bundler project',
        '.csproj': 'C# .NET project',
        '.sln': 'Visual Studio solution',
        'tsconfig.json': 'TypeScript project',
        'webpack.config.js': 'Webpack project',
        'rollup.config.js': 'Rollup project',
        'vite.config.js': 'Vite project'
    }
    
    IGNORE_DIRS = {
        '.git', '.svn', '.hg',
        'node_modules', '__pycache__', '.pytest_cache',
        'target', 'build', 'dist', 'out',
        '.venv', 'venv', 'env',
        '.idea', '.vscode', '.vs',
        'bin', 'obj', '.gradle'
    }
    
    def __init__(self, repo_path: Path):
        """Initialize analyzer with repository path."""
        self.repo_path = repo_path.resolve()
        self.files_by_extension = defaultdict(list)
        self.languages = Counter()
        self.build_files = []
        self.total_files = 0
        self.total_lines = 0
        
    def analyze(self) -> None:
        """Perform full analysis of the repository."""
        print(f"🔍 Analyzing repository: {self.repo_path}")
        print("=" * 60)
        
        self._scan_files()
        self._analyze_languages()
        self._detect_frameworks()
        self._suggest_tasks()
        
    def _scan_files(self) -> None:
        """Scan all files in the repository."""
        for root, dirs, files in os.walk(self.repo_path):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if d not in self.IGNORE_DIRS]
            
            root_path = Path(root)
            for file in files:
                file_path = root_path / file
                relative_path = file_path.relative_to(self.repo_path)
                
                # Skip hidden files and common non-code files
                if file.startswith('.') and file not in ['.gitignore', '.env.example']:
                    continue
                    
                self.total_files += 1
                
                # Categorize by extension
                suffix = file_path.suffix.lower()
                self.files_by_extension[suffix].append(relative_path)
                
                # Count lines for code files
                if suffix in self.LANGUAGE_EXTENSIONS:
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = len(f.readlines())
                            self.total_lines += lines
                            self.languages[self.LANGUAGE_EXTENSIONS[suffix]] += lines
                    except Exception:
                        pass
                
                # Check for build files
                if file.lower() in [f.lower() for f in self.BUILD_FILES]:
                    self.build_files.append((relative_path, self.BUILD_FILES.get(file, 'Unknown')))
    
    def _analyze_languages(self) -> None:
        """Analyze programming languages used."""
        print("📊 Programming Languages (by lines of code):")
        print("-" * 40)
        
        if not self.languages:
            print("  No code files detected")
            return
        
        total_code_lines = sum(self.languages.values())
        for lang, lines in self.languages.most_common():
            percentage = (lines / total_code_lines) * 100
            print(f"  {lang:20} {lines:6,} lines ({percentage:5.1f}%)")
        
        print(f"\nTotal code files: {len([f for ext, files in self.files_by_extension.items() if ext in self.LANGUAGE_EXTENSIONS for f in files])}")
        print(f"Total lines of code: {total_code_lines:,}")
    
    def _detect_frameworks(self) -> None:
        """Detect frameworks and project types."""
        print(f"\n🏗️  Project Structure:")
        print("-" * 40)
        
        if self.build_files:
            print("  Build/Config files found:")
            for file_path, description in self.build_files:
                print(f"    • {file_path} ({description})")
        else:
            print("  No common build files detected")
        
        # Detect common frameworks
        frameworks = []
        
        # Check for common Python frameworks
        if any('python' in lang.lower() for lang in self.languages):
            if any(f.name == 'manage.py' for files in self.files_by_extension.values() for f in files):
                frameworks.append("Django web framework")
            if any('flask' in str(f).lower() for files in self.files_by_extension.values() for f in files):
                frameworks.append("Flask web framework")
            if any('fastapi' in str(f).lower() for files in self.files_by_extension.values() for f in files):
                frameworks.append("FastAPI framework")
        
        # Check for JavaScript frameworks
        if 'package.json' in [f.name for files in self.files_by_extension.values() for f in files]:
            try:
                package_json = self.repo_path / 'package.json'
                if package_json.exists():
                    import json
                    with open(package_json) as f:
                        data = json.load(f)
                        deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
                        
                        if 'react' in deps:
                            frameworks.append("React application")
                        if 'vue' in deps:
                            frameworks.append("Vue.js application")
                        if 'angular' in deps or '@angular/core' in deps:
                            frameworks.append("Angular application")
                        if 'express' in deps:
                            frameworks.append("Express.js server")
                        if 'next' in deps:
                            frameworks.append("Next.js application")
            except Exception:
                pass
        
        if frameworks:
            print(f"\n  Detected frameworks:")
            for framework in frameworks:
                print(f"    • {framework}")
    
    def _suggest_tasks(self) -> None:
        """Suggest tasks the orchestrator could help with."""
        print(f"\n💡 Suggested Tasks for Orchestrator:")
        print("-" * 40)
        
        suggestions = []
        
        # Language-specific suggestions
        if 'Python' in self.languages:
            suggestions.extend([
                "Add comprehensive unit tests for the core modules",
                "Add type hints to improve code maintainability",
                "Add error handling and logging throughout the codebase",
                "Create API documentation using docstrings",
                "Refactor large functions into smaller, more maintainable pieces"
            ])
        
        if any(lang in self.languages for lang in ['JavaScript', 'TypeScript']):
            suggestions.extend([
                "Add Jest unit tests for the main components",
                "Implement error boundaries for better error handling", 
                "Add ESLint configuration and fix linting issues",
                "Optimize performance by implementing proper caching",
                "Add comprehensive end-to-end tests"
            ])
        
        if 'Java' in self.languages:
            suggestions.extend([
                "Add JUnit tests with proper test coverage",
                "Implement proper exception handling patterns",
                "Add comprehensive logging using SLF4J",
                "Refactor to follow SOLID principles",
                "Add integration tests for database operations"
            ])
        
        # Framework-specific suggestions  
        if any('django' in str(f).lower() for files in self.files_by_extension.values() for f in files):
            suggestions.extend([
                "Add Django Rest Framework API endpoints",
                "Implement proper authentication and authorization",
                "Add database migrations for new features",
                "Create management commands for data processing"
            ])
        
        if any('react' in str(f).lower() for files in self.files_by_extension.values() for f in files):
            suggestions.extend([
                "Add React Testing Library tests for components",
                "Implement proper state management with Redux/Zustand",
                "Add accessibility improvements (ARIA labels, etc.)",
                "Optimize bundle size and implement code splitting"
            ])
        
        # General suggestions
        suggestions.extend([
            "Add comprehensive README with setup instructions",
            "Implement CI/CD pipeline with GitHub Actions",
            "Add security audit and vulnerability fixes",
            "Create development environment setup scripts",
            "Add performance monitoring and metrics",
            "Implement database schema migrations",
            "Add API rate limiting and caching",
            "Create user documentation and examples"
        ])
        
        # Show top 10 suggestions
        for i, suggestion in enumerate(suggestions[:10], 1):
            print(f"  {i:2}. {suggestion}")
        
        if len(suggestions) > 10:
            print(f"     ... and {len(suggestions) - 10} more possibilities!")
    
    def get_complexity_score(self) -> Tuple[str, str]:
        """Get a complexity assessment of the repository."""
        if self.total_files < 10:
            return "Simple", "Small project with few files"
        elif self.total_files < 50:
            return "Moderate", "Medium-sized project"
        elif self.total_files < 200:
            return "Complex", "Large project with many components"
        else:
            return "Very Complex", "Enterprise-scale project"


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Analyze a repository for use with the Orchestrator system"
    )
    
    parser.add_argument(
        "directory",
        nargs="?",
        type=Path,
        default=Path.cwd(),
        help="Directory to analyze (default: current directory)"
    )
    
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="Show only a brief summary"
    )
    
    args = parser.parse_args()
    
    target_dir = args.directory.resolve()
    
    if not target_dir.exists():
        print(f"❌ Error: Directory '{target_dir}' does not exist")
        return 1
    
    if not target_dir.is_dir():
        print(f"❌ Error: '{target_dir}' is not a directory")
        return 1
    
    analyzer = RepoAnalyzer(target_dir)
    
    if args.summary_only:
        analyzer._scan_files()
        complexity, desc = analyzer.get_complexity_score()
        print(f"📁 Repository: {target_dir}")
        print(f"📊 Files: {analyzer.total_files}")
        print(f"📈 Complexity: {complexity} ({desc})")
        if analyzer.languages:
            top_lang = analyzer.languages.most_common(1)[0][0]
            print(f"🔤 Primary language: {top_lang}")
    else:
        analyzer.analyze()
        
        complexity, desc = analyzer.get_complexity_score()
        print(f"\n📈 Repository Complexity: {complexity}")
        print(f"   {desc}")
        
        print(f"\n🚀 Ready to use with Orchestrator!")
        print("   Example command:")
        print(f"   python orchestrator_cli.py \"Add unit tests for the core functionality\" --directory \"{target_dir}\"")
    
    return 0


if __name__ == "__main__":
    exit(main())