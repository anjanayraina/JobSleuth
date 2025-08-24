import os
import re
import json
from datetime import datetime, timezone, timedelta
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import MessageEntityTextUrl
from helper.config import ConfigSingleton
from helper.logger import Logger


class TelegramGroupFetcher:
    def __init__(self, groups_path=None):
        self.config = ConfigSingleton()
        self.api_id = self.config.api_id
        self.api_hash = self.config.api_hash
        # Use the session string from the config
        self.string_session = self.config.telegram_string_session
        self.groups_path = groups_path or self.config.groups_path
        self.logger = Logger(__name__)

    def load_groups(self):
        with open(self.groups_path, 'r') as f:
            return json.load(f)

    async def fetch_messages(self, since=None):
        if not self.string_session:
            self.logger.error("TELEGRAM_STRING_SESSION is not set. Skipping Telegram fetch.")
            return []

        groups = self.load_groups()
        results = []
        if not since:
            since = datetime.now(timezone.utc) - timedelta(hours=12)

        async with TelegramClient(StringSession(self.string_session), self.api_id, self.api_hash) as client:
            for group in groups:
                try:
                    self.logger.info(f"Fetching messages from group: {group}")
                    async for message in client.iter_messages(group, limit=250):
                        if message.date >= since and message.text:
                            results.append({
                                "group": group,
                                "date": str(message.date),
                                "text": message.text,
                                "links": self._extract_all_links(message),
                                "source": "telegram"
                            })
                        elif message.date < since:
                            break
                except Exception as e:
                    self.logger.error(f"Could not fetch from Telegram group '{group}': {e}")

        self.logger.info(f"Fetched {len(results)} messages from Telegram.")
        return results

    def _extract_all_links(self, message):
        links = set()
        if getattr(message, "text", None):
            links.update(re.findall(r'https?://[^\s\)]+', message.text))
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