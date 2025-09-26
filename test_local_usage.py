#!/usr/bin/env python3
"""
Test script to verify the local usage functionality works.

This test creates a simple temporary repository and tests the orchestrator on it
without requiring external API calls.
"""

import sys
import tempfile
import shutil
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.agents.env_interaction.command_executor import LocalExecutor
from repo_analyzer import RepoAnalyzer


def test_local_executor():
    """Test that LocalExecutor works correctly."""
    print("🧪 Testing LocalExecutor...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        executor = LocalExecutor(working_directory=temp_dir)
        
        # Test basic command execution
        output, exit_code = executor.execute("echo 'Hello World'")
        assert exit_code == 0
        assert "Hello World" in output
        
        # Test file creation
        output, exit_code = executor.execute("echo 'Test content' > test.txt")
        assert exit_code == 0
        
        # Test file reading
        output, exit_code = executor.execute("cat test.txt")
        assert exit_code == 0
        assert "Test content" in output
        
        print("✅ LocalExecutor tests passed!")


def test_repo_analyzer():
    """Test that RepoAnalyzer works correctly."""
    print("🧪 Testing RepoAnalyzer...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create a simple Python project structure
        (temp_path / "main.py").write_text("""
def hello():
    return "Hello World"

if __name__ == "__main__":
    print(hello())
""")
        
        (temp_path / "test_main.py").write_text("""
import unittest
from main import hello

class TestMain(unittest.TestCase):
    def test_hello(self):
        self.assertEqual(hello(), "Hello World")
""")
        
        (temp_path / "requirements.txt").write_text("pytest>=6.0.0\n")
        
        (temp_path / "README.md").write_text("# Test Project\n\nA simple test project.")
        
        # Test analyzer
        analyzer = RepoAnalyzer(temp_path)
        analyzer._scan_files()
        analyzer._analyze_languages()
        
        assert "Python" in analyzer.languages
        assert analyzer.total_files >= 4  # main.py, test_main.py, requirements.txt, README.md
        
        complexity, desc = analyzer.get_complexity_score()
        assert complexity in ["Simple", "Moderate"]
        
        print("✅ RepoAnalyzer tests passed!")


def test_config_system():
    """Test that configuration system works."""
    print("🧪 Testing configuration system...")
    
    from orchestrator_config import OrchestratorConfig
    
    with tempfile.TemporaryDirectory() as temp_dir:
        config_file = Path(temp_dir) / "test_config.json"
        config = OrchestratorConfig(config_file)
        
        # Test setting and getting values
        config.set("test_key", "test_value")
        assert config.get("test_key") == "test_value"
        
        # Test saving and loading
        config.save()
        assert config_file.exists()
        
        # Load in new instance
        config2 = OrchestratorConfig(config_file)
        assert config2.get("test_key") == "test_value"
        
        print("✅ Configuration system tests passed!")


def test_cli_import():
    """Test that CLI modules can be imported without errors."""
    print("🧪 Testing CLI imports...")
    
    try:
        # Test importing CLI without executing
        import orchestrator_cli
        import orchestrator_config
        import repo_analyzer
        import orchestrator_standalone
        print("✅ CLI import tests passed!")
    except Exception as e:
        print(f"❌ CLI import failed: {e}")
        raise


def main():
    """Run all tests."""
    print("🚀 Testing Local Usage Functionality")
    print("=" * 50)
    
    try:
        test_cli_import()
        test_local_executor()
        test_repo_analyzer()  
        test_config_system()
        
        print("\n" + "=" * 50)
        print("✅ All tests passed!")
        print("🎉 Local usage functionality is working correctly!")
        
        print("\n📋 Next steps:")
        print("1. Set your API key: export LITELLM_API_KEY='your-key'")
        print("2. Analyze a repository: python repo_analyzer.py")
        print("3. Run the orchestrator: python orchestrator_cli.py 'your task'")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()