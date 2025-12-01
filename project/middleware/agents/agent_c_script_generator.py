from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from ..tools.utils import retry_config

SCRIPT_GENERATOR_INSTRUCTIONS = """
Generate a full podcast script based on the plan: {podcast_plan}.
Aim for 1400 words (130-140 wpm).

**[CORRECTION IF EXISTS]:** Address the previous failure reason: {validation_feedback}
"""

ScriptGeneratorAgent = LlmAgent(
    name="ScriptGenerator",
    model=Gemini(model="gemini-1.5-pro", retry_options=retry_config),
    instruction=SCRIPT_GENERATOR_INSTRUCTIONS,
    output_key="generated_script",
)
