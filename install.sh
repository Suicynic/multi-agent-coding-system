#!/bin/bash
# Installation script for the Orchestrator Multi-Agent Coding System.
#
# This script helps users set up the system for use on their own repositories.
#

set -e  # Exit on any error

echo "🤖 Installing Orchestrator Multi-Agent Coding System"
echo "=" * 60

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python version
echo "🐍 Checking Python installation..."
if ! command_exists python3; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3.9 or later from https://python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "✅ Found Python $PYTHON_VERSION"

# Check pip
if ! command_exists pip3 && ! command_exists pip; then
    echo "❌ Error: pip is not installed"
    echo "Please install pip for Python package management"
    exit 1
fi

PIP_CMD="pip3"
if command_exists pip; then
    PIP_CMD="pip"
fi

echo "✅ Found pip"

# Install required dependencies
echo ""
echo "📦 Installing required Python packages..."

REQUIRED_PACKAGES=(
    "litellm>=1.72.6"
    "pyyaml>=6.0.2"  
    "pydantic>=2.11.5"
)

for package in "${REQUIRED_PACKAGES[@]}"; do
    echo "Installing $package..."
    $PIP_CMD install "$package" --user
done

echo "✅ All packages installed successfully!"

# Check if git is available (optional)
if command_exists git; then
    echo "✅ Git is available for version control"
else
    echo "⚠️  Git not found - version control features will be limited"
fi

# Make scripts executable
echo ""
echo "🔧 Setting up executables..."
chmod +x orchestrator_cli.py
chmod +x orchestrator_config.py
chmod +x repo_analyzer.py
chmod +x examples/setup_examples.sh

# Create alias suggestions
echo ""
echo "💡 Optional: Add these aliases to your shell profile for easier usage:"
echo ""
echo "# Add to ~/.bashrc, ~/.zshrc, etc."
echo "alias orchestrator='python3 $(pwd)/orchestrator_cli.py'"
echo "alias orch-config='python3 $(pwd)/orchestrator_config.py'"
echo "alias orch-analyze='python3 $(pwd)/repo_analyzer.py'"

# Environment setup check
echo ""
echo "🌍 Environment Setup:"
if [ -n "$LITELLM_API_KEY" ] || [ -n "$LITE_LLM_API_KEY" ]; then
    echo "✅ API key found in environment"
else
    echo "⚠️  No API key found. Set one of these environment variables:"
    echo "   export LITELLM_API_KEY='your-api-key-here'"
    echo "   export LITE_LLM_API_KEY='your-api-key-here'"
fi

# Create sample configuration
echo ""
echo "⚙️  Configuration:"
echo "Creating sample configuration file..."
python3 orchestrator_config.py --create-sample 2>/dev/null || echo "Configuration system ready"

# Test installation
echo ""
echo "🧪 Testing installation..."
if python3 test_simple.py; then
    echo "✅ Installation test passed!"
else
    echo "❌ Installation test failed"
    exit 1
fi

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "📋 Next Steps:"
echo "1. Set your API key: export LITELLM_API_KEY='your-key'"
echo "2. Analyze a repository: python3 repo_analyzer.py /path/to/project"
echo "3. Run the orchestrator: python3 orchestrator_cli.py 'Add unit tests'"
echo ""
echo "📚 Documentation:"
echo "• Read USAGE.md for detailed instructions"
echo "• Run 'bash examples/setup_examples.sh' for examples"
echo "• Use '--help' with any command for options"
echo ""
echo "🔗 Quick Links:"
echo "• Configuration: python3 orchestrator_config.py --show"
echo "• Examples: ls examples/"
echo "• Help: python3 orchestrator_cli.py --help"