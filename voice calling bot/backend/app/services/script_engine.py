from typing import Dict, Any, List

class ScriptEngine:
    """Manages the progression of conversation stages."""

    def __init__(self):
        # In a real app, this would be parsed from the DB Agent configuration
        self.default_stages = [
            {
                "name": "greeting",
                "goal": "Greet the customer and verify their name.",
                "exit_condition": "Customer confirms their identity."
            },
            {
                "name": "pitch",
                "goal": "Explain the purpose of the call briefly.",
                "exit_condition": "Customer shows interest or asks a question."
            },
            {
                "name": "objection_handling",
                "goal": "Address any concerns.",
                "exit_condition": "Customer is satisfied with answers."
            },
            {
                "name": "closing",
                "goal": "End the call politely.",
                "exit_condition": "Customer says goodbye."
            }
        ]

    def get_current_stage_context(self, current_stage_index: int, custom_script: str = None) -> str:
        """Returns the instructions for the current stage."""
        if custom_script:
            # If a custom script is provided, we just pass the whole thing for MVP
            return f"Follow this script flow: {custom_script}"
            
        if current_stage_index >= len(self.default_stages):
            return "Call is ending. Say goodbye."
            
        stage = self.default_stages[current_stage_index]
        return f"Current Stage: {stage['name']}\nGoal: {stage['goal']}\nExit Condition: Move to next stage when {stage['exit_condition']}"

    def evaluate_transition(self, ai_response: str, user_response: str, current_stage_index: int) -> int:
        """
        Determines if the conversation should move to the next stage.
        In a real app, an LLM would evaluate the exit condition. 
        For MVP, we just aggressively advance if it's a long enough interaction.
        """
        if len(user_response) > 10:
            return min(current_stage_index + 1, len(self.default_stages))
        return current_stage_index

script_engine = ScriptEngine()
