import os
from pathlib import Path
from dotenv import load_dotenv
from google.genai import types

# --- 1. Load Environment Variables ---
# We need to go up two levels from 'utils.py' (tools -> middleware) to find .env
current_file_path = Path(__file__).resolve()
middleware_root = current_file_path.parent.parent
env_path = middleware_root / ".env"

# Load the .env file.
# This injects GOOGLE_API_KEY into the environment so the SDK finds it automatically.
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    print(f"Warning: .env file not found at {env_path}")

# Optional: Verify it loaded
if not os.getenv("GOOGLE_API_KEY"):
    print("Warning: GOOGLE_API_KEY is missing from environment variables.")

# --- 2. Shared Configurations ---
# Your specific retry configuration
retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)
