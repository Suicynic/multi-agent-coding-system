#!/usr/bin/env python3
"""
Orchestrator CLI - Use the multi-agent coding system on any repository.

This CLI allows you to use the Orchestrator multi-agent system on your own repositories,
not just for TerminalBench evaluation.

Usage:
    python orchestrator_cli.py "Add unit tests for the user authentication module"
    python orchestrator_cli.py "Fix the bug in the payment processing logic" --directory /path/to/repo
    python orchestrator_cli.py "Refactor the database connection code" --model "openai/gpt-4" --temperature 0.2
"""

import argparse
import os
import sys
import logging
from pathlib import Path
from typing import Optional

# Add src to path so we can import the orchestrator
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.agents.env_interaction.command_executor import LocalExecutor
from orchestrator_config import OrchestratorConfig
from orchestrator_standalone import StandaloneOrchestrator


def setup_logging(verbose: bool = False):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )


def validate_environment():
    """Validate that required environment variables are set."""
    api_key = os.getenv("LITELLM_API_KEY") or os.getenv("LITE_LLM_API_KEY")
    if not api_key:
        print("❌ Error: No API key found!")
        print("Please set one of these environment variables:")
        print("  - LITELLM_API_KEY")
        print("  - LITE_LLM_API_KEY")
        print()
        print("Example:")
        print("  export LITELLM_API_KEY='your-api-key-here'")
        return False
    
    return True


def validate_directory(directory: Path) -> bool:
    """Validate that the target directory exists and looks like a code repository."""
    if not directory.exists():
        print(f"❌ Error: Directory '{directory}' does not exist.")
        return False
    
    if not directory.is_dir():
        print(f"❌ Error: '{directory}' is not a directory.")
        return False
    
    # Check if it looks like a code repository (has common code files)
    code_indicators = [
        "*.py", "*.js", "*.ts", "*.java", "*.cpp", "*.c", "*.h", 
        "*.go", "*.rs", "*.rb", "*.php", "*.cs", "*.swift",
        "package.json", "requirements.txt", "Cargo.toml", "pom.xml",
        "Makefile", "CMakeLists.txt", ".git"
    ]
    
    has_code = False
    for indicator in code_indicators:
        if list(directory.glob(indicator)) or list(directory.rglob(indicator)):
            has_code = True
            break
    
    if not has_code:
        print(f"⚠️  Warning: Directory '{directory}' doesn't appear to contain code files.")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            return False
    
    return True


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Use the Orchestrator multi-agent coding system on any repository.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Add unit tests for the authentication module"
  %(prog)s "Fix bug in payment processing" --directory /path/to/repo
  %(prog)s "Refactor database code" --model "openai/gpt-4" --temperature 0.2
  %(prog)s "Add error handling" --max-turns 20 --verbose

Configuration:
  Use 'python orchestrator_config.py --create-sample' to create a config file
  Use 'python orchestrator_config.py --show' to view current configuration

Environment Variables:
  LITELLM_API_KEY or LITE_LLM_API_KEY - Your API key for the LLM provider
  LITELLM_MODEL - Default model to use (overridden by --model and config file)
  LITELLM_TEMPERATURE - Default temperature (overridden by --temperature and config file)
  LITELLM_API_BASE - Custom API base URL
        """
    )
    
    parser.add_argument(
        "task",
        help="The coding task you want the orchestrator to complete"
    )
    
    parser.add_argument(
        "--directory", "-d",
        type=Path,
        default=Path.cwd(),
        help="Directory containing the repository to work on (default: current directory)"
    )
    
    parser.add_argument(
        "--model", "-m",
        help="LiteLLM model to use (e.g., 'anthropic/claude-sonnet-4-20250514', 'openai/gpt-4')"
    )
    
    parser.add_argument(
        "--temperature", "-t",
        type=float,
        help="Temperature for LLM responses (0.0 to 1.0)"
    )
    
    parser.add_argument(
        "--max-turns",
        type=int,
        help="Maximum number of turns before stopping (default from config: 50)" 
    )
    
    parser.add_argument(
        "--api-key",
        help="API key for LiteLLM (overrides environment variable)"
    )
    
    parser.add_argument(
        "--api-base",
        help="Custom API base URL for LiteLLM"
    )
    
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to configuration file (default: ~/.orchestrator/config.json)"
    )
    
    parser.add_argument(
        "--logging-dir",
        type=Path,
        help="Directory to save detailed logs (optional)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    parser.add_argument(
        "--show-config",
        action="store_true",
        help="Show current configuration and exit"
    )
    
    args = parser.parse_args()
    
    # Load configuration
    config = OrchestratorConfig(args.config)
    
    # Show configuration if requested
    if args.show_config:
        config.show_config()
        return
    
    # Setup logging
    setup_logging(args.verbose)
    
    # Get effective configuration combining config file, env vars, and CLI args
    effective_config = config.get_effective_config(
        model=args.model,
        temperature=args.temperature,
        api_key=args.api_key,
        api_base=args.api_base,
        max_turns=args.max_turns
    )
    
    # Validate that we have an API key
    if not effective_config.get("api_key"):
        print("❌ Error: No API key found!")
        print("Please set one of these environment variables:")
        print("  - LITELLM_API_KEY")
        print("  - LITE_LLM_API_KEY")
        print()
        print("Or provide it via --api-key argument")
        print()
        print("Example:")
        print("  export LITELLM_API_KEY='your-api-key-here'")
        sys.exit(1)
    
    # Validate directory
    target_directory = args.directory.resolve()
    if not validate_directory(target_directory):
        sys.exit(1)
    
    print("🤖 Orchestrator Multi-Agent Coding System")
    print("=" * 50)
    print(f"📁 Working directory: {target_directory}")
    print(f"🎯 Task: {args.task}")
    print(f"🧠 Model: {effective_config['model']}")
    print(f"🌡️  Temperature: {effective_config['temperature']}")
    print(f"🔄 Max turns: {effective_config['max_turns']}")
    if args.logging_dir:
        print(f"📝 Logging to: {args.logging_dir}")
    print("=" * 50)
    
    try:
        # Create local command executor for the target directory
        executor = LocalExecutor(working_directory=str(target_directory))
        
        # Create orchestrator
        orchestrator = StandaloneOrchestrator(
            model=effective_config["model"],
            temperature=effective_config["temperature"],
            api_key=effective_config["api_key"],
            api_base=effective_config["api_base"]
        )
        
        # Setup orchestrator with local executor
        orchestrator.setup(executor, args.logging_dir)
        
        print("\n🚀 Starting orchestration...")
        print("The orchestrator will coordinate explorer and coder agents to complete your task.\n")
        
        # Run the task
        result = orchestrator.run(args.task, max_turns=effective_config["max_turns"])
        
        # Display results
        print("\n" + "=" * 50)
        print("📊 EXECUTION RESULTS")
        print("=" * 50)
        
        if result['completed']:
            print("✅ Task completed successfully!")
            print(f"📝 Result: {result['finish_message']}")
        else:
            print("⚠️  Task did not complete within the turn limit")
            if result['finish_message']:
                print(f"📝 Last message: {result['finish_message']}")
        
        print(f"🔄 Turns executed: {result['turns_executed']}")
        print(f"⏰ Max turns reached: {result['max_turns_reached']}")
        
        if args.logging_dir:
            print(f"📝 Detailed logs saved to: {args.logging_dir}")
        
        # Show token usage if available
        if hasattr(orchestrator, 'orchestrator_messages'):
            try:
                from src.agents.utils.llm_client import count_input_tokens, count_output_tokens
                
                total_input_tokens = sum(count_input_tokens(msg['content'], effective_config["model"]) 
                                       for msg in orchestrator.orchestrator_messages 
                                       if msg['role'] in ['system', 'user'])
                total_output_tokens = sum(count_output_tokens(msg['content'], effective_config["model"]) 
                                        for msg in orchestrator.orchestrator_messages 
                                        if msg['role'] == 'assistant')
                
                print(f"🪙 Tokens used: {total_input_tokens} input + {total_output_tokens} output = {total_input_tokens + total_output_tokens} total")
            except Exception as e:
                logging.debug(f"Could not calculate token usage: {e}")
        
    except KeyboardInterrupt:
        print("\n⏹️  Execution stopped by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()