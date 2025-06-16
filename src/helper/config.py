import os
from dotenv import load_dotenv

class ConfigSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Get absolute path to project root (parent of helpers/)
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            env_path = os.path.join(project_root, 'resources', '.env')
            load_dotenv(env_path)
            cls._instance.api_id = int(os.getenv('ID'))
            cls._instance.api_hash = os.getenv('APP_HASH')
        return cls._instance
