# fetchers/telegram_group_fetcher.py
import json
from datetime import datetime, timedelta, timezone
from telethon.sync import TelegramClient
from helper.config import ConfigSingleton

class JobPostFilter:
    def __init__(self, min_length=30, min_keyword_matches=2):
        self.keywords = [
            "hiring", "we are hiring", "open position", "looking for",
            "job", "vacancy", "opening", "role", "position",
            "join our team", "apply", "send your cv", "remote", "onsite",
            "developer", "engineer", "designer", "internship", "recruiting", "career",
            "full-time", "part-time", "contract", "salary"
        ]
        self.min_length = min_length
        self.min_keyword_matches = min_keyword_matches

    def is_job_post(self, text: str) -> bool:
        if not text or len(text) < self.min_length:
            return False
        text_lower = text.lower()
        hits = sum(kw in text_lower for kw in self.keywords)
        return hits >= self.min_keyword_matches

class TelegramGroupFetcher:
    def __init__(self, groups_path='resources/groups.json'):
        self.config = ConfigSingleton()
        self.api_id = self.config.api_id
        self.api_hash = self.config.api_hash
        self.groups = self._load_groups(groups_path)
        self.session_name = "fetch24hr_session"
        self.job_filter = JobPostFilter()

    def _load_groups(self, path):
        with open(path, 'r') as f:
            return json.load(f)

    def fetch_last_24_hours(self):
        now = datetime.now(timezone.utc)
        since = now - timedelta(hours=24)
        results = []
        with TelegramClient(self.session_name, self.api_id, self.api_hash) as client:
            for group in self.groups:
                print(f"\n====== Fetching messages from: {group} ======")
                for message in client.iter_messages(group):
                    if message.date >= since and message.text:
                        if self.job_filter.is_job_post(message.text):
                            sender = message.sender
                            sender_name = getattr(sender, 'first_name', None) or getattr(sender, 'title', 'Unknown')
                            results.append({
                                "group": group,
                                "sender": sender_name,
                                "date": str(message.date),
                                "text": message.text
                            })
                    elif message.date < since:
                        break
        return results
