from apscheduler.schedulers.blocking import BlockingScheduler
from fetchers.telegram_group_fetcher import TelegramGroupFetcher
from extractors.extract_job_fields import extract_job_fields
from extractors.tagger import extract_tags
from helper.db import MongoDB
from helper.logger import Logger
from datetime import datetime

log = Logger()
db = MongoDB()

async def fetch_and_store_jobs():
    log.info("Starting scheduled job fetch...")
    fetcher = TelegramGroupFetcher()
    messages = await fetcher.fetch_messages()
    log.info(f"Fetched {len(messages)} messages.")

    for message in messages:
        job_data = extract_job_fields(message["text"])
        if job_data:
            job_data["tags"] = extract_tags(job_data["description"])
            job_data["source"] = "telegram"
            job_data["fetched_at"] = datetime.utcnow().isoformat()
            db.insert_job(job_data)
            log.info(f"Inserted job: {job_data['title']} at {job_data['company']}")

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(fetch_and_store_jobs, 'interval', minutes=30)
    log.info("Scheduler started. Press Ctrl+C to exit.")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        log.info("Scheduler stopped.")
