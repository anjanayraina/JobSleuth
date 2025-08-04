# services/job_search_service.py
from services.mongodb_service import MongoDBService
from models.job_search_request import JobSearchRequest
import re

class JobSearchService:
    def __init__(self, collection_name='jobs'):
        self.db = MongoDBService(collection_name)

    def build_query(self, request: JobSearchRequest):
        query = {}

        if request.general_query:
            regex = re.compile(re.escape(request.general_query), re.IGNORECASE)
            query["$or"] = [
                {"title": regex},
                {"description": regex},
                {"company": regex}
            ]
        if request.tags:
            query["tags"] = {"$in": [tag.lower() for tag in request.tags]}
        if request.location:
            query["location"] = {"$regex": re.escape(request.location), "$options": "i"}
        if request.job_type:
            query["job_type"] = {"$regex": re.escape(request.job_type), "$options": "i"}
        if request.company:
            query["company"] = {"$regex": re.escape(request.company), "$options": "i"}

        if request.min_salary is not None or request.max_salary is not None:
            salary_query = {}
            if request.min_salary is not None:
                salary_query["$gte"] = request.min_salary
            if request.max_salary is not None:
                salary_query["$lte"] = request.max_salary
            if salary_query:
                query["salary_num"] = salary_query

        return query
    @staticmethod
    def serialize_mongo_doc(doc):
        doc = dict(doc)
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])
        return doc

    def search_jobs(self, request: JobSearchRequest):
        query = self.build_query(request)
        jobs = [self.serialize_mongo_doc(job) for job in self.db.jobs_col.find(
            query,
            limit=request.limit,
            skip=request.skip,
            sort=[("date_posted", -1)]
        )]

        return jobs
