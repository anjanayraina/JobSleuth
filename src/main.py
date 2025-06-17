from fastapi import FastAPI
from routes.job_route import router as jobs_router
from scheduler.runner import start_scheduler
from helper.logger import Logger
import threading

log = Logger()
app = FastAPI(title="JobPilot Backend")
app.include_router(jobs_router)

@app.on_event("startup")
def on_startup():
    thread = threading.Thread(target=start_scheduler, daemon=True)
    thread.start()
    log.info("Scheduler started in background.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
