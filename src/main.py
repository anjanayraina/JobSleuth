import yaml
import logging.config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.job_route import router as jobs_router
from routes.job_search import router as job_search_router
from routes.auth_route import router as auth_router


with open("log_conf.yaml", 'r') as f:
    log_config = yaml.safe_load(f)
    logging.config.dictConfig(log_config)
# ------------------------------------

log = logging.getLogger(__name__)
app = FastAPI(title="JobSleuth Backend")

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

app.include_router(auth_router, prefix="/api")
app.include_router(jobs_router, prefix="/api")
app.include_router(job_search_router, prefix="/api")

