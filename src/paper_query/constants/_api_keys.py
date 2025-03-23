from chatbots.utils import load_api_keys

# Load the API keys
api_keys = load_api_keys()

OPENAI_API_KEY = api_keys.get("OPENAI_API_KEY", None)
