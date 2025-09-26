#!/usr/bin/env python3
"""
Standalone Orchestrator that can be used without TerminalBench dependencies.

This is a simplified version of the OrchestratorAgent that removes the TerminalBench
coupling, making it usable on any repository.
"""

import json
import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import sys
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.agents.actions.orchestrator_hub import OrchestratorHub
from src.agents.actions.parsing.action_handler import ActionHandler
from src.agents.actions.state_managers import ScratchpadManager, TodoManager
from src.agents.env_interaction.entities.conversation_history import ConversationHistory
from src.agents.env_interaction.entities.turn import Turn
from src.agents.env_interaction.turn_executor import TurnExecutor
from src.agents.actions.parsing.parser import SimpleActionParser

from src.agents.utils.llm_client import (
    count_input_tokens,
    count_output_tokens,
    get_llm_response,
)

from src.agents.state.orchestrator_state import OrchestratorState
from src.agents.env_interaction.command_executor import CommandExecutor
from src.misc.log_setup import setup_file_logging
from src.misc.turn_logger import TurnLogger
from src.agents.system_msgs.system_msg_loader import load_orchestrator_system_message

logger = logging.getLogger(__name__)
setup_file_logging("INFO")


class StandaloneOrchestrator:
    """Standalone orchestrator agent for use on any repository."""
    
    def __init__(
        self,
        system_message_path: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
    ):
        """Initialize the orchestrator.
        
        Args:
            system_message_path: Path to system message file
            model: LiteLLM model to use (overrides env var)
            temperature: Temperature for LLM (overrides env var)
            api_key: API key for LiteLLM (overrides env var)
            api_base: API base URL for LiteLLM (overrides env var)
        """
        # Store LLM configuration
        self.model = model
        self.temperature = temperature
        self.api_key = api_key
        self.api_base = api_base
        
        logger.info(f"StandaloneOrchestrator initialized with model={model}, temperature={temperature}")
        
        # Load system message
        self.system_message = self._load_system_message(system_message_path)
        
        # These will be initialized in setup()
        self.orchestrator_hub = None
        self.conversation_history = None
        self.action_parser = None
        self.action_handler = None
        self.executor = None
        self.state = None
        
        # Track orchestrator's messages for token counting
        self.orchestrator_messages = []
        
        # Turn logger (will be initialized in perform_task)
        self.turn_logger = None
        self.logging_dir = None
    
    def _load_system_message(self, path: Optional[str]) -> str:
        if path:
            # If explicit path provided, load from that file
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            # Use default system message loader
            return load_orchestrator_system_message()
    
    def setup(self, command_executor: CommandExecutor, logging_dir: Optional[Path] = None):
        """Setup the orchestrator with the necessary components.
        
        Args:
            command_executor: The command executor to use
            logging_dir: Optional directory for logging
        """
        
        # Initialize components with the provided executor
        self.orchestrator_hub = OrchestratorHub()
        self.conversation_history = ConversationHistory()
        
        # Store logging directory
        self.logging_dir = logging_dir
        
        # Create action components
        self.action_parser = SimpleActionParser()
        self.action_handler = ActionHandler(
            executor=command_executor,
            todo_manager=TodoManager(),
            scratchpad_manager=ScratchpadManager(),
            orchestrator_hub=self.orchestrator_hub,
            model=self.model,
            temperature=self.temperature,
            api_key=self.api_key,
            api_base=self.api_base,
            logging_dir=logging_dir,  # Pass logging dir for subagent logging
        )
        
        # Store executor
        self.executor = command_executor
        
        # Initialize state
        self.state = OrchestratorState()
        
        # Initialize turn logger if logging directory provided
        if logging_dir:
            self.turn_logger = TurnLogger(logging_dir, "orchestrator")
    
    def execute_turn(self, instruction: str, turn_num: int) -> Dict[str, Any]:
        """Execute a single orchestrator turn.
        
        Args:
            instruction: The main task instruction
            turn_num: Current turn number
            
        Returns:
            Dictionary with turn results
        """
        # Build user message with context
        conversation_context = self.conversation_history.to_string()
        state_context = self.state.to_string()
        
        user_message = f"""
MAIN TASK: {instruction}

CONVERSATION HISTORY:
{conversation_context}

CURRENT STATE:
{state_context}

What action would you like to take next?
"""
        
        # Get LLM response
        llm_response = self._get_llm_response(user_message)
        
        # Execute turn
        turn_executor = TurnExecutor(
            action_parser=self.action_parser,
            action_handler=self.action_handler
        )
        
        result = turn_executor.execute_turn(
            user_message=user_message,
            llm_response=llm_response,
            state=self.state
        )
        
        # Create turn object
        turn = Turn(
            turn_number=turn_num,
            user_message=user_message,
            llm_response=llm_response,
            actions_executed=result.actions_executed,
            env_responses=result.env_responses,
            subagent_trajectories=result.subagent_trajectories
        )
        
        # Add to conversation history
        self.conversation_history.add_turn(turn)
        
        # Log this turn if logger is available
        if self.turn_logger:
            turn_data = {
                "instruction": instruction,
                "user_message": user_message,
                "llm_response": llm_response,
                "actions_executed": [str(action) for action in result.actions_executed],
                "env_responses": result.env_responses,
                "subagent_trajectories": result.subagent_trajectories,
                "done": result.done,
                "finish_message": result.finish_message,
                "has_error": result.has_error,
                "state_snapshot": self.state.to_dict()
            }
            self.turn_logger.log_turn(turn_num, turn_data)
        
        # Update done state
        if result.done:
            self.state.done = True
            self.state.finish_message = result.finish_message
            logging.info(f"🟡 ORCHESTRATOR: Task marked as DONE - {result.finish_message}")
        else:
            logging.info(f"🟡 ORCHESTRATOR TURN {turn_num} COMPLETE - Continuing...\n")
        
        return {
            'done': result.done,
            'finish_message': result.finish_message,
            'has_error': result.has_error,
            'actions_executed': len(result.actions_executed),
            'turn': turn
        }
    
    def _get_llm_response(self, user_message: str) -> str:
        # Build messages for this request
        messages = [
            {"role": "system", "content": self.system_message},
            {"role": "user", "content": user_message}
        ]
        
        # Track messages for token counting (add system message only once)
        if not self.orchestrator_messages:
            self.orchestrator_messages.append({"role": "system", "content": self.system_message})
        self.orchestrator_messages.append({"role": "user", "content": user_message})
        
        # Call centralized LLM client
        response = get_llm_response(
            messages=messages,
            model=self.model,
            temperature=self.temperature,
            max_tokens=4096,
            api_key=self.api_key,
            api_base=self.api_base
        )
        
        # Track assistant response
        self.orchestrator_messages.append({"role": "assistant", "content": response})
        
        return response
    
    def run(self, instruction: str, max_turns: int = 50) -> Dict[str, Any]:
        """Run the orchestrator until completion or max turns.
        
        Args:
            instruction: The main task to complete
            max_turns: Maximum number of turns before stopping
            
        Returns:
            Final execution summary
        """
        turns_executed = 0
        
        while not self.state.done and turns_executed < max_turns:
            turns_executed += 1
            logger.info(f"Executing turn {turns_executed}")
            logging.info(f"\n{'='*60}")
            logging.info(f"ORCHESTRATOR MAIN LOOP - Turn {turns_executed}/{max_turns}")
            logging.info(f"{'='*60}")
            
            try:
                result = self.execute_turn(instruction, turns_executed)
                
                if result['done']:
                    logger.info(f"Task completed: {result['finish_message']}")
                    break
                    
            except Exception as e:
                logger.error(f"Error in turn {turns_executed}: {e}")
                # Could add error to conversation history here
                
        return {
            'completed': self.state.done,
            'finish_message': self.state.finish_message,
            'turns_executed': turns_executed,
            'max_turns_reached': turns_executed >= max_turns
        }