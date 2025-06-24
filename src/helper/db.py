from pymongo import MongoClient
from helper.config import ConfigSingleton

class MongoDB:
    def __init__(self):
        config = ConfigSingleton()
        self.client = MongoClient(config.mongodb_uri)
        self.db = self.client['jobsleuth']
        self.jobs_col = self.db['jobs']

    def insert_job(self, job):
        return self.jobs_col.insert_one(job)

    def find_jobs(self, query=None):
        return list(self.jobs_col.find(query or {}))
