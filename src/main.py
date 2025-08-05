from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.job_route import router as jobs_router
from routes.job_search import router as job_search_router
from routes.auth_route import router as auth_router # 1. Import the auth router
from helper.logger import Logger

log = Logger(__name__)
app = FastAPI(title="JobPilot Backend")

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(jobs_router)
app.include_router(job_search_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
