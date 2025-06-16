from fastapi import FastAPI, Query
from typing import List
from fetchers import (
    fetch_remoteok,
    fetch_remotive,
    fetch_weworkremotely,
    fetch_crypto_jobs
)
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
    sources: List[str] = Query(default=["remoteok", "remotive", "weworkremotely", "cryptojobs"], description="Sources to search")
):
    all_jobs = []
    if "remoteok" in sources:
        all_jobs += fetch_remoteok(keywords)
    if "remotive" in sources:
        all_jobs += fetch_remotive(keywords)
    if "weworkremotely" in sources:
        all_jobs += fetch_weworkremotely(keywords)
    if "cryptojobs" in sources:
        all_jobs += fetch_crypto_jobs(keywords)
    jobs = dedupe_jobs(all_jobs)
    return jobs
