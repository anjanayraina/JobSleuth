# tests/services/test_job_search_service.py

import pytest
import mongomock

from services.job_search_service import JobSearchService
from models.job_search_request import JobSearchRequest

@pytest.fixture
def job_search_service():
    # Setup mongomock client and fake collection
    mock_client = mongomock.MongoClient()
    db = mock_client['testdb']
    jobs_col = db['jobs']

    # Insert some test data
    jobs_col.insert_many([
        {
            "title": "Python Backend Developer",
            "company": "Google",
            "description": "Develop APIs with Python and FastAPI.",
            "tags": ["python", "backend"],
            "location": "Remote",
            "job_type": "full time",
            "salary": "100000",
            "job_hash": "hash1"
        },
        {
            "title": "React Frontend Developer",
            "company": "Meta",
            "description": "Work on React projects.",
            "tags": ["react", "frontend"],
            "location": "Bangalore",
            "job_type": "part time",
            "salary": "50000",
            "job_hash": "hash2"
        },
        {
            "title": "Data Scientist",
            "company": "OpenAI",
            "description": "Data science with Python.",
            "tags": ["python", "data science"],
            "location": "San Francisco",
            "job_type": "contract",
            "salary": "120000",
            "job_hash": "hash3"
        }
    ])

    # Patch the JobSearchService to use the mock collection
    service = JobSearchService()
    service.db.jobs_col = jobs_col
    return service

def test_general_query(job_search_service):
    req = JobSearchRequest(general_query="python")
    jobs = job_search_service.search_jobs(req)
    assert len(jobs) == 2
    assert all("python" in (job["title"].lower() + job["description"].lower()) for job in jobs)

def test_tag_query(job_search_service):
    req = JobSearchRequest(tags=["backend"])
    jobs = job_search_service.search_jobs(req)
    assert len(jobs) == 1
    assert jobs[0]["title"] == "Python Backend Developer"

def test_location_query(job_search_service):
    req = JobSearchRequest(location="Bangalore")
    jobs = job_search_service.search_jobs(req)
    assert len(jobs) == 1
    assert jobs[0]["company"] == "Meta"

def test_job_type_query(job_search_service):
    req = JobSearchRequest(job_type="full time")
    jobs = job_search_service.search_jobs(req)
    assert len(jobs) == 1
    assert jobs[0]["company"] == "Google"

def test_company_query(job_search_service):
    req = JobSearchRequest(company="OpenAI")
    jobs = job_search_service.search_jobs(req)
    assert len(jobs) == 1
    assert jobs[0]["title"] == "Data Scientist"



def test_pagination(job_search_service):
    req = JobSearchRequest(limit=1, skip=1)
    jobs = job_search_service.search_jobs(req)
    assert len(jobs) == 1

def test_multi_filter(job_search_service):
    req = JobSearchRequest(
        general_query="python",
        tags=["data science"],
        location="San Francisco",
        job_type="contract"
    )
    jobs = job_search_service.search_jobs(req)
    assert len(jobs) == 1
    assert jobs[0]["company"] == "OpenAI"

def test_no_match(job_search_service):
    req = JobSearchRequest(company="NonExistentCompany")
    jobs = job_search_service.search_jobs(req)
    assert len(jobs) == 0
