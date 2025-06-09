from fastapi import FastAPI, Query
from typing import List
from fetchers import fetch_remoteok, fetch_wellfound
from models.job import Job

app = FastAPI(title="JobPilot Backend")

def dedupe_jobs(jobs):
    seen = set()
    unique = []
    for job in jobs:
        key = (job["title"], job["company"], job["link"])
        if key not in seen:
            seen.add(key)
            unique.append(job)
    return unique

@app.get("/fetch_jobs", response_model=List[Job])
def fetch_jobs(
    keywords: List[str] = Query(default=["python"], description="List of keywords"),
    sources: List[str] = Query(default=["remoteok", "wellfound"], description="Sources to search")
):
    all_jobs = []
    if "remoteok" in sources:
        all_jobs += fetch_remoteok(keywords)
    if "wellfound" in sources:
        all_jobs += fetch_wellfound(keywords)
    # Add more sources here
    jobs = dedupe_jobs(all_jobs)
    return jobs
