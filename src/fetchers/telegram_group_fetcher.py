from telethon import TelegramClient
from telethon.tl.types import MessageEntityTextUrl
import json
from datetime import datetime, timezone, timedelta
from helper.config import ConfigSingleton
from helper.logger import Logger
from extractors.regex_extractor import extract_url
import re

class TelegramGroupFetcher:
    def __init__(self, groups_path=None):
        self.config = ConfigSingleton()
        self.api_id = self.config.api_id
        self.api_hash = self.config.api_hash
        # If groups_path provided, use it; else use config value
        self.groups_path = groups_path or self.config.groups_path
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
                        links = self.extract_all_links(message)
                        results.append({
                            "group": group,
                            "date": str(message.date),
                            "text": message.text,
                            "links": links
                        })
                    elif message.date < since:
                        break
        self.logger.info(f"Fetched {len(results)} messages.")
        return results

    def extract_all_links(self, message):
        links = set()

        if getattr(message, "text", None):
            url_pattern = r'https?://[^\s\)\]]+'
            links.update(re.findall(url_pattern, message.text))

        if getattr(message, "entities", None):
            for entity in message.entities:
                if isinstance(entity, MessageEntityTextUrl):
                    links.add(entity.url)

        if getattr(message, "reply_markup", None):
            for row in message.reply_markup.rows:
                for button in row.buttons:
                    if hasattr(button, "url") and button.url:
                        links.add(button.url)

        return list(links)
