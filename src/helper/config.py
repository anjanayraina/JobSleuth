import os
from dotenv import load_dotenv

class ConfigSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            env_type = os.getenv('ENV_TYPE', 'dev')
            env_file = os.path.join(os.path.dirname(__file__), '..', 'resources', f'.env.{env_type}')
            load_dotenv(dotenv_path=env_file)
            cls._instance.api_id = int(os.getenv('ID'))
            cls._instance.api_hash = os.getenv('APP_HASH')
            cls._instance.mongodb_uri = os.getenv('MONGODB_URI')
            cls._instance.groups_path = os.getenv('GROUPS_PATH', '../resources/groups.json')
            cls._instance.openrouter_api_key = os.getenv('OPEN_ROUTER_KEY')
            cls._instance.job_collection_name = os.getenv('JOB_COLLECTION_NAME')
            cls._instance.jwt_secret_key = os.getenv('JWT_SECRET_KEY')
            cls._instance.jwt_algorithm = os.getenv('JWT_ALGORITHM' , 'HS256')
            cls._instance.hugging_face_api = os.getenv('HUGGING_FACE_API')
            cls._instance.telegram_string_session = os.getenv('TELEGRAM_STRING_SESSION')

        return cls._instance
