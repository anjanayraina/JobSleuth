from fastapi import FastAPI
from routes.job_route import router as jobs_router
from scheduler.runner import start_scheduler
import threading

app = FastAPI(title="JobPilot Backend")
app.include_router(jobs_router)

@app.on_event("startup")
def on_startup():
    # Start scheduler in a background thread so it doesn't block FastAPI
    thread = threading.Thread(target=start_scheduler, daemon=True)
    thread.start()
    print("✅ Scheduler started in background.")

# Optional: add shutdown event if you want to gracefully stop scheduler

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
