import asyncio
from fetchers.telegram_group_fetcher import TelegramGroupFetcher
from services.job_extractor_service import JobExtractorService
from services.mongodb_service import MongoDBService
from helper.logger import Logger


class JobsWorkflowService:
    def __init__(self, collection_name=None):
        self.extractor = JobExtractorService()
        self.db = MongoDBService(collection_name)
        self.logger = Logger(__name__)
        self.fetchers = [
            TelegramGroupFetcher(),
        ]

    async def run_workflow(self):
        self.logger.info("Starting job fetch workflow for all sources...")

        # Concurrently fetch messages from all sources
        fetch_tasks = [fetcher.fetch_messages() for fetcher in self.fetchers]
        results = await asyncio.gather(*fetch_tasks, return_exceptions=True)

        all_messages = []
        for i, result in enumerate(results):
            fetcher_name = self.fetchers[i].__class__.__name__
            if isinstance(result, Exception):
                self.logger.error(f"Failed to fetch from {fetcher_name}: {result}")
            else:
                self.logger.info(f"Fetched {len(result)} messages from {fetcher_name}")
                all_messages.extend(result)

        self.logger.info(f"Total messages fetched: {len(all_messages)}")

        # Let the extractor service handle the entire batch with its hybrid logic
        processed_jobs = self.extractor.process_messages_in_batches(all_messages)

        # Filter out jobs that already exist in the database
        jobs_to_insert = []
        for job in processed_jobs:
            if not self.db.job_exists(job.job_hash):
                jobs_to_insert.append(job.model_dump())

        if jobs_to_insert:
            num_inserted = self.db.insert_many(jobs_to_insert)
            self.logger.info(f"Successfully inserted {num_inserted} new jobs into the database.")
            return num_inserted
        else:
            self.logger.info("No new valid jobs found to insert.")
            return 0