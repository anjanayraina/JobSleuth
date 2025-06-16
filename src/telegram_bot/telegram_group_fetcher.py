import json
from datetime import datetime, timedelta, timezone
from telethon.sync import TelegramClient
from helper.config import ConfigSingleton

class TelegramGroupFetcher:
    def __init__(self, groups_path='../resources/groups.json'):
        self.config = ConfigSingleton()
        self.api_id = self.config.api_id
        self.api_hash = self.config.api_hash
        self.groups = self._load_groups(groups_path)
        self.session_name = "fetch24hr_session"

    def _load_groups(self, path):
        with open(path, 'r') as f:
            return json.load(f)

    def fetch_last_24_hours(self):
        now = datetime.now(timezone.utc)
        since = now - timedelta(hours=48)
        results = []
        with TelegramClient(self.session_name, self.api_id, self.api_hash) as client:
            for group in self.groups:
                print(f"\n====== Fetching messages from: {group} ======")
                for message in client.iter_messages(group):
                    if message.date >= since and message.text:
                        sender = message.sender
                        sender_name = getattr(sender, 'first_name', None) or getattr(sender, 'title', 'Unknown')
                        print(f"From: {sender_name}")
                        print(f"Date: {message.date}")
                        print(f"Text: {message.text}")
                        print('-' * 40)
                        results.append({
                            "group": group,
                            "sender": sender_name,
                            "date": str(message.date),
                            "text": message.text
                        })
                    elif message.date < since:
                        break
        print("\n✅ Done fetching messages from all groups!")
        return results

# --- Usage Example ---
if __name__ == "__main__":
    fetcher = TelegramGroupFetcher(groups_path='../resources/groups.json')
    messages = fetcher.fetch_last_24_hours()
    # You can now save `messages` to a file, database, etc.
