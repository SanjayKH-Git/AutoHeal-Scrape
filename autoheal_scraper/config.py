import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration from environment variables
ORIGINAL_URL = os.getenv('ORIGINAL_URL', 'http://127.0.0.1:5000')
UPDATED_URL = os.getenv('UPDATED_URL', 'http://127.0.0.1:5000/updated')

# LLM provider selection: 'gemini', 'openai' or 'anthropic'
LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'gemini')

# API Keys (from environment variables)
# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
# ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')