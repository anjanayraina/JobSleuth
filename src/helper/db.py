from pymongo import MongoClient
import os

class MongoDB:
    def __init__(self, uri=None, db_name="job_db"):
        uri = uri or os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db.jobs

    def insert_job(self, job):
        if not self.collection.find_one({"link": job["link"]}):
            self.collection.insert_one(job)

    def find_jobs(self, query={}, limit=100):
        return list(self.collection.find(query).limit(limit))
