import asyncio
import inspect
import uuid

# Import agents
from .agents.agent_a_trends import TopicFinderAgent
from .agents.agent_b_plan_creator import PlanCreatorAgent
from .agents.agent_c_script_generator import ScriptGeneratorAgent
from .agents.agent_d_script_validator import ScriptValidatorAgent
from .agents.agent_e_audio_generator import AudioGeneratorAgent
from .agents.refinement_loop import ScriptRefinementLoop

# Instantiate the Custom Loop
critique_loop = ScriptRefinementLoop(
    name="ScriptRefinementLoop",
    generator=ScriptGeneratorAgent,
    validator=ScriptValidatorAgent,
    max_iterations=3,
)

# Pipeline steps
pipeline_steps = [
    TopicFinderAgent,
    PlanCreatorAgent,
    critique_loop,
    AudioGeneratorAgent,
]

# --- 🛡️ BULLETPROOF ADK EMULATION LAYER ---


class MockRunConfig:
    """
    Satisfies invocation_context.run_config checks.
    """

    def __init__(self):
        self.response_modalities = []
        self.speech_config = None
        self.output_audio_transcription = False
        # 🔴 FINAL FIX: Add the missing input transcription flag
        self.input_audio_transcription = False


class MockPluginManager:
    """Satisfies the ADK's plugin and resource system hooks."""

    async def run_before_agent_callback(self, *args, **kwargs):
        return None

    async def run_after_agent_callback(self, *args, **kwargs):
        return None

    async def run_before_model_callback(self, *args, **kwargs):
        return None

    async def run_after_model_callback(self, *args, **kwargs):
        return None

    async def run_before_tool_callback(self, *args, **kwargs):
        return None

    async def run_after_tool_callback(self, *args, **kwargs):
        return None

    async def run_on_model_error_callback(self, *args, **kwargs):
        return None


class MockSession:
    """Satisfies the ADK's session and history tracking."""

    def __init__(self, state: dict):
        self.id = str(uuid.uuid4())
        self.state = state
        self.history = []


class UniversalContext:
    """
    A comprehensive mock of InvocationContext.
    """

    def __init__(self, state: dict):
        # 1. Core Data
        self.state = state
        self.session = MockSession(state)

        # 2. Lifecycle & Identity
        self.invocation_id = str(uuid.uuid4())
        self.agent = None
        self.end_invocation = False

        # 3. Internal Agent Memory
        self.agent_states = {}

        # 4. System Dependencies
        self.plugin_manager = MockPluginManager()
        self.resource_manager = MockPluginManager()
        self.trace_span = None
        self.user = "script_user"

        # 5. Runtime Configuration
        self.run_config = MockRunConfig()

    def model_copy(self, update=None):
        """
        Allows LlmAgent to 'clone' the context while maintaining shared state.
        """
        if update and "agent" in update:
            self.agent = update["agent"]
        return self


# --- 🚀 PIPELINE EXECUTION ---


async def run_pipeline():
    initial_data = {"user_segment": "Japan", "exclude_list": ["politics", "finance"]}

    # Initialize the robust context
    current_context = UniversalContext(state=initial_data)

    print("\n🚀 Starting Podcast Generation Pipeline (Context Mode)...\n")

    try:
        for i, agent in enumerate(pipeline_steps):
            agent_name = getattr(agent, "name", f"Agent_{i}")
            print(f"▶️ Executing Step {i+1}: {agent_name}...")

            # Execute Agent
            if hasattr(agent, "run_async"):
                result = agent.run_async(current_context)

                # Handle Streaming (LlmAgent) vs Coroutine (CustomAgent)
                if inspect.isasyncgen(result):
                    async for _ in result:
                        pass
                else:
                    await result

            elif hasattr(agent, "run"):
                agent.run(current_context)
            else:
                print(
                    f"❌ Critical Error: Agent '{agent_name}' has no execution method!"
                )
                break

            # Print keys from the context's state to show progress
            current_keys = list(current_context.state.keys())
            print(f"   ✅ Step Complete. State keys: {current_keys}")

        # Final Extraction
        final_state = current_context.state
        print("\n\n=== 🏁 FINAL PIPELINE STATE ===")
        print({k: v for k, v in final_state.items() if k != "history"})

        if final_state.get("audio_generated"):
            path = final_state.get("audio_file_path")
            print(f"\n🎉 SUCCESS! Podcast Audio generated at:\n👉 {path}")
        else:
            print("\n⚠️ Pipeline finished, but no audio file was generated.")

    except Exception as e:
        print(f"\n❌ Pipeline Crashed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(run_pipeline())
