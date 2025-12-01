
## 🎙️ AI Podcast Content Generator

An end-to-end, self-correcting pipeline that identifies trending topics, drafts compliant, long-form scripts, and generates finished, multi-speaker audio files using advanced Google Gemini models.

-----

## 🌟 Project Overview

This project solves the **slow, manual grind of creating high-quality, topical podcast content**. Instead of relying on manual research and error-prone drafting, we use a chain of specialized AI agents to automate the entire process, featuring a crucial **self-critique loop** for guaranteed quality control.

### Why Agents?

We use agents because the task requires **specialized reasoning** and **error correction**—a single massive prompt just won't cut it. Each agent acts as a specialist: one for research (using Google Search), one for quality control (using code logic), and another for audio synthesis (using the TTS model).

-----

## 🧠 Architecture: The Self-Correcting Pipeline

The system is built as a **Sequential, Asynchronous Pipeline** where state is passed and refined at each step.

| Step | Agent / Component | Function | Key Output |
| :--- | :--- | :--- | :--- |
| **1. Research** | **TopicFinder (LlmAgent)** | Identifies a fresh, relevant trend based on user input (e.g., target market/segment). | `{selected_topic}` |
| **2. Planning** | **PlanCreator (LlmAgent)** | Generates a structured, time-compliant outline. | `{podcast_plan}` |
| **3. Refinement** | **ScriptRefinementLoop (Custom Agent)** | **The core engine.** Cycles the Generator and Validator (max 3 times). | Final `{generated_script}` |
| **4. Validation** | **ScriptValidator (LlmAgent)** | Audits the script for length (using Python's `len()`) and quality. Returns **"VALID"** to stop the loop or a precise error reason. | `{validation_feedback}` |
| **5. Generation** | **AudioGenerator (Custom Agent)** | Uses the verified script to call the Gemini TTS API, generating the final audio bytes. | `{audio_file_path}` |

-----

## 🛠️ Key Technologies & Implementation

  * **Models:** **Gemini 1.5 Pro** (for drafting), **Gemini 1.5 Flash** (for planning/validation), **Gemini 2.5 Pro TTS** (for audio output).
  * **Orchestration:** Manual Python orchestration using **`asyncio`** to handle the asynchronous nature of the agents.
  * **Tooling:** Integrated `Google Search` tool and custom Python functions for deterministic tasks (like word counting).
  * **Context Emulation (The Build Tax):** To run the pipeline as a single script instead of a full server app, we implemented a **`UniversalContext` Mock Class** to emulate the complex internal dependencies (like `session`, `plugin_manager`, and `run_config`) that the ADK requires.

-----

## 💻 Setup and Execution

### Prerequisites

1.  Python (3.11 or later recommended).
2.  An active Gemini API Key.
3.  Install Dependencies:
    ```bash
    pip install google-adk google-genai python-dotenv
    ```

### Configuration

1.  Create a `.env` file inside the `middleware/` directory.
2.  Add your API key:
    ```
    GOOGLE_API_KEY="AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    ```

### Run the Pipeline

Execute the pipeline from the project root directory using the module flag:

```bash
python -m middleware.pipeline
```

### Expected Output

The script will show debug messages for each step, including loop attempts. Upon completion, it will print the final state and a path to the generated file:

```
▶️ Executing Step 3: ScriptRefinementLoop...
...
Validation Feedback: Word count is 350. Must be between 500 and 2000 words.
Loop Iteration 2/3
Validation Feedback: VALID
>>> Verification Successful! Exiting Loop.
...
🎉 SUCCESS! Podcast Audio generated at:
👉 final_podcast.wav
```

-----

## 🔮 Future Improvements

If given more development time, the following features would be added:

1.  **Cost Optimization Router:** Implement a routing agent to use the most cost-effective Gemini model for each stage (e.g., use **Flash** for planning, only switching to **Pro** for final drafting).
2.  **External Storage:** Integrate with Google Cloud Storage (GCS) to automatically upload the final `.wav` file for easy distribution.
3.  **Real-time Data Integration:** Enhance the planner with tools to fetch and integrate real-time data (e.g., current stock prices, weather, sports scores) into the script, making the content fresh.
