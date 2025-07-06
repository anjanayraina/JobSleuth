from fetchers.telegram_group_fetcher import TelegramGroupFetcher
from services.job_extractor_service import JobExtractorService
from helper.mongodb_service import MongoDBService
from helper.logger import Logger
from datetime import datetime, timezone
import asyncio

class JobsWorkflowService:
    def __init__(self, collection_name=None):
        self.fetcher = TelegramGroupFetcher()
        self.extractor = JobExtractorService()
        self.db = MongoDBService(collection_name)
        self.logger = Logger()

    async def run_workflow(self):
        self.logger.info("Starting job fetch workflow")
        messages = await self.fetcher.fetch_messages()
        self.logger.info(f"Fetched {len(messages)} messages")

        jobs_to_insert = []
        for msg in messages:
            job = self.extractor.extract_job_fields(msg)
            if job:
                job_dict = job.dict()
                job_dict["source"] = "telegram"
                job_dict["fetched_at"] = datetime.now(timezone.utc).isoformat()
                jobs_to_insert.append(job_dict)
            else:
                self.logger.debug(f"Skipping message: {msg.get('text', '')[:60]}...")

        if jobs_to_insert:
            self.db.insert_many(jobs_to_insert)
            self.logger.info(f"Inserted {len(jobs_to_insert)} jobs to the database")
        else:
            self.logger.info("No valid jobs found to insert")
        return len(jobs_to_insert)
if __name__ == "__main__":
    workflow = JobsWorkflowService()
    num_inserted = asyncio.run(workflow.run_workflow())
    print(num_inserted)
