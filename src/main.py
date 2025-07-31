from fastapi import FastAPI
from routes.job_route import router as jobs_router
from routes.job_search import router as job_search_router
from helper.logger import Logger
import threading

log = Logger()
app = FastAPI(title="JobPilot Backend")
app.include_router(jobs_router)
app.include_router(job_search_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
