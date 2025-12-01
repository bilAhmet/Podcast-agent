from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from ..tools.utils import retry_config

PLAN_CREATOR_INSTRUCTIONS = """
Create a detailed, 5-10 minute podcast episode plan/outline covering the topic: {selected_topic}.
"""

PlanCreatorAgent = LlmAgent(
    name="PlanCreator",
    model=Gemini(model="gemini-1.5-flash", retry_options=retry_config),
    instruction=PLAN_CREATOR_INSTRUCTIONS,
    output_key="podcast_plan",
)
