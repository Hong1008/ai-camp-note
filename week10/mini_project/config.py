import os
from pathlib import Path
from dotenv import load_dotenv

# Base Directory of the mini project
MINI_PROJECT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = MINI_PROJECT_DIR.parent.parent

# Load .env file from the project root
load_dotenv(dotenv_path=PROJECT_ROOT / '.env')

# LLM Configuration
GOOGLE_AI_API_KEY = os.getenv("GOOGLE_AI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", GOOGLE_AI_API_KEY)  # Fallback to Google key if needed

# Endpoints
# By default, use Google Gemini OpenAI-compatible endpoint
# For local models, this can be set to "http://localhost:11434/v1" (Ollama) or "http://localhost:8000/v1" (vLLM)
DEFAULT_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
BASE_URL = os.getenv("LLM_BASE_URL", DEFAULT_BASE_URL)

# Model Selection
# "gemma-4-31b-it" is the default reasoning model
# DEFAULT_MODEL_NAME = "gemma-4-31b-it"
DEFAULT_MODEL_NAME = "gemini-3.1-flash-lite"
MODEL_NAME = os.getenv("LLM_MODEL_NAME", DEFAULT_MODEL_NAME)
AVAILABLE_MODELS = ["gemini-3.1-flash-lite", "gemma-4-31b-it"]


# Hyperparameters
DEFAULT_TEMPERATURE = 1.0
DEFAULT_TOP_P = 0.95
DEFAULT_TOP_K = 64
DEFAULT_MAX_TOKENS = 2048
DEFAULT_TIMEOUT = 30.0


# Data Files Paths
QUESTION_BANK_PATH = MINI_PROJECT_DIR / "data" / "question.json"
PERSONA_PATH = MINI_PROJECT_DIR / "data" / "persona.json"
