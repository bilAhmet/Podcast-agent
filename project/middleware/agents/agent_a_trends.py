from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search

from ..tools.utils import retry_config

TREND_DISCOVERY_INSTRUCTIONS = """
Analyze current Google search trends for the segment '{user_segment}' and exclude any topics in the provided '{exclude_list}'.
If '{exclude_list}' is empty or not provided, you don't need to exclude any topics.
Return only the single, most relevant trending topic.
"""

# Agent A: Topic Finder
TopicFinderAgent = LlmAgent(
    name="TopicFinder",
    model=Gemini(model="gemini-1.5-flash", retry_options=retry_config),
    instruction=TREND_DISCOVERY_INSTRUCTIONS,
    tools=[google_search],
    output_key="selected_topic",
)
