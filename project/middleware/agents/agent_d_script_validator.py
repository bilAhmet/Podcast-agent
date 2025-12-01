from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from ..tools.utils import retry_config
from ..tools.word_counter import word_counter_tool

SCRIPT_VALIDATOR_INSTRUCTIONS = """
Your task is to validate the provided script: {generated_script}.

1. First, use the `count_words` tool to get the exact word count.
2. Check two things:
   a. Word Count: Must be between 500 and 2000 words.
   b. Quality Score: Must be > 5/10.

Output Instructions:
- If BOTH checks pass, return exactly the word: VALID
- If ANY check fails, return ONLY the reason for failure (max 50 words). Do not include JSON.

Example Success: VALID
Example Failure: Word count is 350, which is below the minimum.
"""

ScriptValidatorAgent = LlmAgent(
    name="ScriptValidator",
    model=Gemini(model="gemini-1.5-flash", retry_options=retry_config),
    instruction=SCRIPT_VALIDATOR_INSTRUCTIONS,
    tools=[word_counter_tool],
    output_key="validation_feedback",
)
