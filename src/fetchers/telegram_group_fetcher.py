from telethon import TelegramClient  # no `.sync`
import json
from datetime import datetime, timezone, timedelta
from helper.config import ConfigSingleton
from helper.logger import Logger

class TelegramGroupFetcher:
    def __init__(self):
        self.config = ConfigSingleton()
        self.api_id = self.config.api_id
        self.api_hash = self.config.api_hash
        self.groups_path = self.config.groups_path
        self.session_name = "telegram_fetcher_session.session"
        self.logger = Logger()

    def load_groups(self):
        with open(self.groups_path, 'r') as f:
            return json.load(f)

    async def fetch_messages(self, since=None):
        groups = self.load_groups()
        results = []
        if not since:
            since = datetime.now(timezone.utc) - timedelta(hours=48)
        async with TelegramClient(self.session_name, self.api_id, self.api_hash) as client:
            for group in groups:
                self.logger.info(f"Fetching messages from group: {group}")
                async for message in client.iter_messages(group):
                    if message.date >= since and message.text:
                        results.append({
                            "group": group,
                            "date": str(message.date),
                            "text": message.text
                        })
                    elif message.date < since:
                        break
        self.logger.info(f"Fetched {len(results)} messages.")
        return results
