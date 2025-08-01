from fastapi import FastAPI
# 1. Import the CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
from routes.job_route import router as jobs_router
from routes.job_search import router as job_search_router
from helper.logger import Logger
import threading

log = Logger()
app = FastAPI(title="JobPilot Backend")

# --- CORS Middleware Configuration ---

# 2. Define the list of frontend URLs that are allowed to connect.
#    This is your "guest list".
origins = [
    "http://localhost:5173",  # Your React frontend's address
    # You can add your live website's URL here later
    # e.g., "https://www.jobsleuth.com"
]

# 3. Add the middleware to your FastAPI app.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- End of CORS Configuration ---

app.include_router(jobs_router)
app.include_router(job_search_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
