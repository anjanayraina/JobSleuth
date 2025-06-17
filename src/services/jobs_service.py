# services/jobs_service.py
from helper.db import MongoDB

def get_jobs_service(tags=None):
    db = MongoDB()
    query = {}
    if tags:
        query["tags"] = {"$in": tags.split(",")}
    return db.find_jobs(query)
