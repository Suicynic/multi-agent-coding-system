#!/usr/bin/env python3
"""
Simple test to verify the basic structure is working.
"""

import tempfile
from pathlib import Path


def test_local_executor_basic():
    """Test basic LocalExecutor functionality without full imports."""
    print("🧪 Testing basic LocalExecutor structure...")
    
    # Read the command executor file to verify our LocalExecutor class exists
    cmd_executor_file = Path(__file__).parent / "src" / "agents" / "env_interaction" / "command_executor.py"
    
    if not cmd_executor_file.exists():
        raise FileNotFoundError(f"Command executor file not found: {cmd_executor_file}")
    
    content = cmd_executor_file.read_text()
    
    # Check that our LocalExecutor class is defined
    assert "class LocalExecutor(CommandExecutor):" in content
    assert "def __init__(self, working_directory: str = None):" in content
    assert "def execute(self, cmd: str, timeout: int = 30)" in content
    
    print("✅ LocalExecutor class structure verified!")


def test_cli_files_exist():
    """Test that all CLI files exist."""
    print("🧪 Testing CLI files exist...")
    
    base_dir = Path(__file__).parent
    
    required_files = [
        "orchestrator_cli.py",
        "orchestrator_config.py", 
        "orchestrator_standalone.py",
        "repo_analyzer.py",
        "USAGE.md",
        "examples/basic_usage.py",
        "examples/setup_examples.sh"
    ]
    
    for file_path in required_files:
        full_path = base_dir / file_path
        assert full_path.exists(), f"Required file missing: {file_path}"
        
        # Check that files are not empty
        if full_path.suffix == ".py":
            content = full_path.read_text()
            assert len(content) > 100, f"File {file_path} seems too small"
    
    print("✅ All required CLI files exist and have content!")


def test_repo_analyzer_structure():
    """Test RepoAnalyzer structure without full imports."""
    print("🧪 Testing repo_analyzer structure...")
    
    analyzer_file = Path(__file__).parent / "repo_analyzer.py"
    content = analyzer_file.read_text()
    
    # Check key components exist
    assert "class RepoAnalyzer:" in content
    assert "def analyze(self)" in content
    assert "def _scan_files(self)" in content
    assert "def _suggest_tasks(self)" in content
    
    print("✅ RepoAnalyzer structure verified!")


def test_usage_documentation():
    """Test that usage documentation exists and is comprehensive."""
    print("🧪 Testing usage documentation...")
    
    usage_file = Path(__file__).parent / "USAGE.md"
    content = usage_file.read_text()
    
    # Check key sections exist
    required_sections = [
        "Quick Start",
        "Installation", 
        "CLI Interface",
        "Repository Analysis",
        "Task Examples",
        "Environment Variables",
        "Troubleshooting"
    ]
    
    for section in required_sections:
        assert section in content, f"Missing section in USAGE.md: {section}"
    
    # Check it has substantial content
    assert len(content) > 5000, "USAGE.md seems too short"
    
    print("✅ Usage documentation verified!")


def main():
    """Run all tests."""
    print("🚀 Testing Local Usage Functionality (Simple)")
    print("=" * 50)
    
    try:
        test_cli_files_exist()
        test_local_executor_basic()
        test_repo_analyzer_structure()
        test_usage_documentation()
        
        print("\n" + "=" * 50)
        print("✅ All basic structure tests passed!")
        print("🎉 The local usage functionality structure is correct!")
        
        print("\n📋 What we've created:")
        print("• orchestrator_cli.py - Main CLI interface")
        print("• orchestrator_standalone.py - TerminalBench-free orchestrator")
        print("• orchestrator_config.py - Configuration management")
        print("• repo_analyzer.py - Repository analysis tool")
        print("• LocalExecutor - Local filesystem command execution")
        print("• USAGE.md - Comprehensive usage documentation")
        print("• examples/ - Usage examples and templates")
        
        print("\n🚀 Ready to use! Set LITELLM_API_KEY and try:")
        print("python orchestrator_cli.py 'Add unit tests for core functionality'")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())