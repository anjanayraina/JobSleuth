from pymongo import MongoClient, errors
from helper import ConfigSingleton
from helper.logger import Logger

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
            Logger().error(f"Index creation error: {e}")

    def insert_job(self, job_dict):
        try:
            self.jobs_col.insert_one(job_dict)
            return True
        except errors.DuplicateKeyError:
            Logger().info(f"Duplicate job detected (hash: {job_dict.get('job_hash')})")
            return False

    def insert_many(self, job_dicts):
        if not job_dicts:
            return 0
        try:
            result = self.jobs_col.insert_many(job_dicts, ordered=False)
            return len(result.inserted_ids)
        except errors.BulkWriteError as bwe:
            inserted = len([op for op in bwe.details['writeErrors'] if op['code'] != 11000])
            Logger().info(f"Bulk write with duplicates. Inserted: {inserted}")
            return inserted

    def job_exists(self, job_hash):
        return self.jobs_col.find_one({"job_hash": job_hash}) is not None

    def fetch_all_jobs(self):
        return list(self.jobs_col.find())
