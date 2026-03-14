import os
from dotenv import load_dotenv

load_dotenv()

# API key — set via .env file or environment variable
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Model configuration
MANAGER_MODEL  = "claude-opus-4-20250514"   # Smarter model for planning & review
DEVELOPER_MODEL = "claude-sonnet-4-20250514" # Fast model for execution

# Flask
SECRET_KEY = os.getenv("SECRET_KEY", "ideasmith-secret")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
