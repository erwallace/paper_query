from paper_query.utils import load_api_keys

# Load the API keys
api_keys = load_api_keys()

OPENAI_API_KEY = api_keys.get("OPENAI_API_KEY", None)
HUGGINGFACE_API_KEY = api_keys.get("HUGGINGFACE_API_KEY", None)
GROQ_API_KEY = api_keys.get("GROQ_API_KEY", None)
