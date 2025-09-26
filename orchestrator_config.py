#!/usr/bin/env python3
"""
Configuration management for the Orchestrator CLI.

This module handles loading and saving configuration for the orchestrator,
making it easier for users to set up their preferred models, API keys, etc.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class OrchestratorConfig:
    """Manages configuration for the Orchestrator CLI."""
    
    DEFAULT_CONFIG = {
        "model": "anthropic/claude-sonnet-4-20250514",
        "temperature": 0.1,
        "max_turns": 50,
        "api_base": None,
        "default_logging": False
    }
    
    def __init__(self, config_file: Optional[Path] = None):
        """Initialize configuration manager.
        
        Args:
            config_file: Path to configuration file. If None, uses default location.
        """
        if config_file is None:
            # Use default config location in user's home directory
            config_file = Path.home() / ".orchestrator" / "config.json"
        
        self.config_file = config_file
        self._config = self.DEFAULT_CONFIG.copy()
        self.load()
    
    def load(self) -> None:
        """Load configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    self._config.update(loaded_config)
                logger.debug(f"Loaded configuration from {self.config_file}")
            except Exception as e:
                logger.warning(f"Failed to load configuration from {self.config_file}: {e}")
                logger.warning("Using default configuration")
    
    def save(self) -> None:
        """Save current configuration to file."""
        try:
            # Create directory if it doesn't exist
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_file, 'w') as f:
                json.dump(self._config, f, indent=2)
            logger.debug(f"Saved configuration to {self.config_file}")
        except Exception as e:
            logger.error(f"Failed to save configuration to {self.config_file}: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self._config[key] = value
    
    def get_effective_config(self, 
                           model: Optional[str] = None,
                           temperature: Optional[float] = None,
                           api_key: Optional[str] = None,
                           api_base: Optional[str] = None,
                           max_turns: Optional[int] = None) -> Dict[str, Any]:
        """Get effective configuration, combining config file, environment variables, and CLI overrides.
        
        Args:
            model: CLI override for model
            temperature: CLI override for temperature
            api_key: CLI override for API key
            api_base: CLI override for API base
            max_turns: CLI override for max turns
            
        Returns:
            Dictionary with effective configuration
        """
        # Start with config file values
        config = self._config.copy()
        
        # Override with environment variables
        env_model = os.getenv("LITELLM_MODEL")
        if env_model:
            config["model"] = env_model
        
        env_temperature = os.getenv("LITELLM_TEMPERATURE")
        if env_temperature:
            try:
                config["temperature"] = float(env_temperature)
            except ValueError:
                logger.warning(f"Invalid LITELLM_TEMPERATURE value: {env_temperature}")
        
        env_api_base = os.getenv("LITELLM_API_BASE")
        if env_api_base:
            config["api_base"] = env_api_base
        
        # Get API key from environment (required)
        env_api_key = os.getenv("LITELLM_API_KEY") or os.getenv("LITE_LLM_API_KEY")
        config["api_key"] = env_api_key
        
        # Override with CLI arguments
        if model is not None:
            config["model"] = model
        if temperature is not None:
            config["temperature"] = temperature
        if api_key is not None:
            config["api_key"] = api_key
        if api_base is not None:
            config["api_base"] = api_base  
        if max_turns is not None:
            config["max_turns"] = max_turns
        
        return config
    
    def show_config(self) -> None:
        """Print current configuration."""
        print("📋 Current Configuration:")
        print("-" * 30)
        for key, value in self._config.items():
            if key == "api_key":
                # Don't show the full API key for security
                display_value = f"{value[:8]}..." if value else "Not set"
            else:
                display_value = value
            print(f"  {key}: {display_value}")
        print(f"\n📁 Config file: {self.config_file}")
        
        # Show environment variables
        print("\n🌍 Environment Variables:")
        env_vars = {
            "LITELLM_MODEL": os.getenv("LITELLM_MODEL"),
            "LITELLM_TEMPERATURE": os.getenv("LITELLM_TEMPERATURE"), 
            "LITELLM_API_KEY": os.getenv("LITELLM_API_KEY"),
            "LITE_LLM_API_KEY": os.getenv("LITE_LLM_API_KEY"),
            "LITELLM_API_BASE": os.getenv("LITELLM_API_BASE")
        }
        
        for key, value in env_vars.items():
            if value:
                if "API_KEY" in key:
                    display_value = f"{value[:8]}..." if len(value) > 8 else "***"
                else:
                    display_value = value
                print(f"  {key}: {display_value}")
            else:
                print(f"  {key}: Not set")


def create_sample_config():
    """Create a sample configuration file with comments."""
    config = OrchestratorConfig()
    
    sample_config_with_comments = {
        "_comment": "Orchestrator Configuration File",
        "_description": "This file contains default settings for the Orchestrator CLI",
        "model": "anthropic/claude-sonnet-4-20250514",
        "_model_options": [
            "anthropic/claude-sonnet-4-20250514",
            "openai/gpt-4",
            "openai/gpt-4-turbo",
            "openrouter/qwen/qwen3-coder",
            "openrouter/deepseek/deepseek-chat-v3.1"
        ],
        "temperature": 0.1,
        "_temperature_note": "Lower values (0.0-0.3) for more focused/deterministic responses, higher (0.7-1.0) for more creative",
        "max_turns": 50,
        "_max_turns_note": "Maximum number of orchestrator turns before stopping",
        "api_base": None,
        "_api_base_note": "Custom API base URL if using a different provider",
        "default_logging": False,
        "_logging_note": "Whether to enable detailed logging by default"
    }
    
    # Create directory if it doesn't exist
    config.config_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(config.config_file, 'w') as f:
            json.dump(sample_config_with_comments, f, indent=2)
        print(f"✅ Created sample configuration file: {config.config_file}")
        print("Edit this file to customize your default settings.")
    except Exception as e:
        logger.error(f"Failed to create sample configuration: {e}")


if __name__ == "__main__":
    # CLI for configuration management
    import argparse
    
    parser = argparse.ArgumentParser(description="Manage Orchestrator configuration")
    parser.add_argument("--show", action="store_true", help="Show current configuration")
    parser.add_argument("--create-sample", action="store_true", help="Create a sample configuration file")
    parser.add_argument("--set", nargs=2, metavar=("KEY", "VALUE"), help="Set a configuration value")
    
    args = parser.parse_args()
    
    if args.create_sample:
        create_sample_config()
    elif args.show:
        config = OrchestratorConfig()
        config.show_config()
    elif args.set:
        config = OrchestratorConfig()
        key, value = args.set
        
        # Try to convert common types
        if value.lower() in ("true", "false"):
            value = value.lower() == "true"
        elif value.isdigit():
            value = int(value)
        elif value.replace(".", "", 1).isdigit():
            value = float(value)
        elif value.lower() == "none":
            value = None
        
        config.set(key, value)
        config.save()
        print(f"✅ Set {key} = {value}")
    else:
        parser.print_help()