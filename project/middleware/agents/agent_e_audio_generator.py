import base64
import os
from typing import Any  # 🔴 FIX: Added missing import
from google.adk.agents import Agent
from google.genai import Client, types
from ..tools.utils import retry_config

client = Client(api_key=os.environ.get("GOOGLE_API_KEY"))


class AudioGeneratorCustomAgent(Agent):
    """
    Async version of the Audio Generator, updated for InvocationContext.
    """

    output_filename: str = "final_podcast.wav"
    model_id: str = "gemini-2.0-flash-exp"

    async def run_async(self, context) -> Any:
        print(f"\n--- 🎙️ Agent E: Generating Audio ({self.output_filename}) ---")

        # Access state via .state property
        script = context.state.get("generated_script", "")
        if not script:
            print("Error: No script found to convert.")
            return context

        prompt = (
            "Read the following podcast script aloud. "
            "Use a multi-speaker style if possible, with an engaging, professional tone.\n\n"
            f"{script}"
        )

        try:
            # Call the API directly
            response = client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name="Puck"
                            )
                        )
                    ),
                ),
            )

            audio_bytes = None
            if response.candidates and response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if part.inline_data:
                        audio_bytes = part.inline_data.data
                        break

            if audio_bytes:
                if isinstance(audio_bytes, str):
                    audio_data = base64.b64decode(audio_bytes)
                else:
                    audio_data = audio_bytes

                with open(self.output_filename, "wb") as f:
                    f.write(audio_data)

                print(
                    f"✅ Success! Audio saved to: {os.path.abspath(self.output_filename)}"
                )
                context.state["audio_file_path"] = self.output_filename
                context.state["audio_generated"] = True
            else:
                print("❌ Error: No audio data found.")
                context.state["audio_generated"] = False

        except Exception as e:
            print(f"❌ Error generating audio: {e}")
            context.state["audio_generated"] = False

        return context


AudioGeneratorAgent = AudioGeneratorCustomAgent(
    name="AudioGenerator", output_filename="final_podcast.wav"
)
