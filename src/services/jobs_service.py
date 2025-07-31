# services/jobs_service.py
from helper.mongodb_service import MongoDBService

def get_jobs_service(tags=None):
    db = MongoDBService()
    query = {}
    if tags:
        query["tags"] = {"$in": tags.split(",")}
    return db.find_jobs(query)
