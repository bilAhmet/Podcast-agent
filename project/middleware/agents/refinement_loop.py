import inspect
from typing import Any
from google.adk.agents import Agent


class ScriptRefinementLoop(Agent):
    """
    Async version of the custom loop agent, updated for InvocationContext.
    """

    generator: Any
    validator: Any
    max_iterations: int = 3

    # 🔴 FIX: Accept 'context', not 'state'
    async def run_async(self, context) -> Any:
        print(
            f"\n--- Starting Refinement Loop (Max {self.max_iterations} attempts) ---"
        )

        for i in range(self.max_iterations):
            print(f"Loop Iteration {i+1}/{self.max_iterations}")

            # 1. Run Generator (Pass Context)
            if hasattr(self.generator, "run_async"):
                result = self.generator.run_async(context)
                if inspect.isasyncgen(result):
                    async for ctx in result:
                        context = ctx
                else:
                    context = await result

            # 2. Run Validator (Pass Context)
            if hasattr(self.validator, "run_async"):
                result = self.validator.run_async(context)
                if inspect.isasyncgen(result):
                    async for ctx in result:
                        context = ctx
                else:
                    context = await result

            # 3. Check Condition (Read from context.state)
            feedback = context.state.get("validation_feedback", "").strip()
            print(f"Validation Feedback: {feedback}")

            if feedback == "VALID":
                print(">>> Verification Successful! Exiting Loop.")
                break
            else:
                print(">>> Verification Failed. Retrying...")

        return context
