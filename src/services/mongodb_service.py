from bson import ObjectId
from pymongo import MongoClient, errors
from helper.config import ConfigSingleton
from helper.logger import Logger


log = Logger(__name__)

class MongoDBService:
    def __init__(self, collection_name=None):
        config = ConfigSingleton()
        self.client = MongoClient(config.mongodb_uri)
        db_name = self.client.get_default_database().name
        self.db = self.client[db_name]
        self.collection_name = collection_name or "jobs"
        self.jobs_col = self.db[self.collection_name]

        try:
            self.jobs_col.create_index("job_hash", unique=True)
        except errors.OperationFailure as e:
            log.error(f"Index creation error: {e}")

    def insert_job(self, job_dict):
        try:
            self.jobs_col.insert_one(job_dict)
            return True
        except errors.DuplicateKeyError:
            log.info(f"Duplicate job detected (hash: {job_dict.get('job_hash')})")
            return False

    def insert_many(self, job_dicts):
        if not job_dicts:
            return 0
        try:
            result = self.jobs_col.insert_many(job_dicts, ordered=False)
            return len(result.inserted_ids)
        except errors.BulkWriteError as bwe:
            inserted = bwe.details['nInserted']
            log.info(f"Bulk write with duplicates. Inserted: {inserted}")
            return inserted

    def job_exists(self, job_hash):
        return self.jobs_col.find_one({"job_hash": job_hash}) is not None

    def find_jobs(self, query=None):
        return list(self.jobs_col.find(query or {}))

    def get_user_by_email(self, email: str):
        users_col = self.db["users"] # Use a separate collection for users
        return users_col.find_one({"email": email})

    def find_job_by_id(self, job_id: str):
        try:
            return self.jobs_col.find_one({"_id": ObjectId(job_id)})
        except Exception:
            return None
    def create_user(self, user_data: dict):
        users_col = self.db["users"]
        try:
            users_col.insert_one(user_data)
            return True
        except errors.DuplicateKeyError:
            log.warning(f"User with email {user_data.get('email')} already exists.")
            return False
