from fetchers.telegram_group_fetcher import TelegramGroupFetcher
from services.job_extractor_service import JobExtractorService
from services.mongodb_service import MongoDBService
from helper.logger import Logger
import asyncio


class JobsWorkflowService:
    def __init__(self, collection_name=None):
        self.fetcher = TelegramGroupFetcher()
        self.extractor = JobExtractorService()
        self.db = MongoDBService(collection_name)
        self.logger = Logger(__name__)

    async def run_workflow(self):
        self.logger.info("Starting job fetch workflow...")
        messages = await self.fetcher.fetch_messages()

        processed_jobs = self.extractor.process_messages_in_batches(messages)

        jobs_to_insert = []
        for job in processed_jobs:
            if not self.db.job_exists(job.job_hash):
                jobs_to_insert.append(job.model_dump())

        if jobs_to_insert:
            num_inserted = self.db.insert_many(jobs_to_insert)
            self.logger.info(f"Successfully inserted {num_inserted} new jobs into the database.")
        else:
            self.logger.info("No new valid jobs found to insert.")

        return len(jobs_to_insert)


if __name__ == "__main__":
    workflow = JobsWorkflowService()
    num_inserted = asyncio.run(workflow.run_workflow())
    print(f"Workflow finished. Inserted {num_inserted} new jobs.")