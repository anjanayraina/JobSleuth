from fastapi import FastAPI
from routes.job_route import router as jobs_router

app = FastAPI(title="JobPilot Backend")
app.include_router(jobs_router)
