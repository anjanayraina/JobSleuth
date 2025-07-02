import os
from dotenv import load_dotenv

class ConfigSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'resources', '.env'))
            cls._instance.api_id = int(os.getenv('ID'))
            cls._instance.api_hash = os.getenv('APP_HASH')
            cls._instance.mongodb_uri = os.getenv('MONGODB_URI')
            cls._instance.groups_path = os.getenv('GROUPS_PATH', 'resources/groups.json')
            cls._instance.openrouter_api_key = os.getenv('OPEN_ROUTER_KEY')

        return cls._instance
