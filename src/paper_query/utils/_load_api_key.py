import os


def load_api_keys(file_path: str = "~/.config/my_api_keys") -> dict:
    """Function to load API keys from the file."""
    api_key_file_path = os.path.expanduser(file_path)

    api_keys = {}
    if not os.path.exists(api_key_file_path):
        raise FileNotFoundError(f"API key file not found at {file_path}")
    else:
        with open(api_key_file_path) as file:
            for line in file:
                if line.strip() and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    api_keys[key] = value

    return api_keys
