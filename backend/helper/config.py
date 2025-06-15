import os
from dotenv import load_dotenv

class ConfigSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            # Only create once
            cls._instance = super(ConfigSingleton, cls).__new__(cls)
            # Load the .env file from resources
            env_path = os.path.join(os.path.dirname(__file__), 'resources', '.env')
            load_dotenv(env_path)
            cls._instance.api_id = int(os.getenv('API_ID'))
            cls._instance.api_hash = os.getenv('API_HASH')
            cls._instance.group = os.getenv('GROUP')
        return cls._instance