import os
from dotenv import load_dotenv

class ConfigSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            load_dotenv()
            cls._instance.api_id = int(os.getenv('API_ID'))
            cls._instance.api_hash = os.getenv('API_HASH')
            cls._instance.mongodb_uri = os.getenv('MONGODB_URI')
            cls._instance.telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
            cls._instance.groups_path = os.getenv('GROUPS_PATH', 'resources/groups.json')
        return cls._instance
