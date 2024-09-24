from .configs.config import OPENAI_API_KEY
def get_openai_api_key() -> str:
    """Retrieve OpenAI API key from config."""
    return OPENAI_API_KEY
