from apscheduler.schedulers.background import BackgroundScheduler
from helper.config import ConfigSingleton
from fetchers.telegram_group_fetcher import TelegramGroupFetcher
from extractors.tagger import extract_tags
from helper.db import MongoDB
from helper.logger import Logger
from datetime import datetime
from services.job_extractor_service import JobExtractorService
import os
import json

log = Logger()
db = MongoDB()
extractor = JobExtractorService()
config = ConfigSingleton()

def load_last_scrape_time():
    if os.path.exists(config.last_scrape_path):
        with open(config.last_scrape_path, "r") as f:
            data = json.load(f)
            return datetime.fromisoformat(data["last_scrape"])
    from datetime import timezone, timedelta
    return datetime.now(timezone.utc) - timedelta(hours=48)

def save_last_scrape_time(dt):
    with open(config.last_scrape_path, "w") as f:
        json.dump({"last_scrape": dt.isoformat()}, f)

async def fetch_and_store_jobs():
    log.info("Starting scheduled job fetch...")
    last_scrape = load_last_scrape_time()
    fetcher = TelegramGroupFetcher()
    messages = await fetcher.fetch_messages(since=last_scrape)
    log.info(f"Fetched {len(messages)} messages since {last_scrape}.")

    new_last_scrape = last_scrape
    for message in messages:
        msg_time = datetime.fromisoformat(message["date"]) if "date" in message else None
        if msg_time and msg_time > new_last_scrape:
            new_last_scrape = msg_time

        job_obj = extractor.extract_job_fields(message)
        if job_obj:
            job_dict = job_obj.dict()
            job_dict["tags"] = extract_tags(job_obj.description)
            job_dict["source"] = "telegram"
            job_dict["fetched_at"] = datetime.utcnow().isoformat()
            db.insert_job(job_dict)
            log.info(f"Inserted job: {job_obj.title} at {job_obj.company}")

    save_last_scrape_time(new_last_scrape)

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_and_store_jobs, 'interval', minutes=30)
    scheduler.start()
    log.info("Background scheduler running.")
