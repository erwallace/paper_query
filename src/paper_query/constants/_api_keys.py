import os

from paper_query.utils import load_api_keys

keys = ["OPENAI_API_KEY", "HUGGINGFACE_API_KEY", "GROQ_API_KEY"]
# This is needed so that during GitHub actions testing, the API keys can be loaded from the ci.yaml
# via secrets.
if not all(os.environ.get(key) for key in keys):
    api_keys = load_api_keys()

    OPENAI_API_KEY = api_keys.get("OPENAI_API_KEY")
    HUGGINGFACE_API_KEY = api_keys.get("HUGGINGFACE_API_KEY")
    GROQ_API_KEY = api_keys.get("GROQ_API_KEY")

else:
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    HUGGINGFACE_API_KEY = os.environ.get("HUGGINGFACE_API_KEY")
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
