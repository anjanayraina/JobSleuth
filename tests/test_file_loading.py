from fetchers.telegram_group_fetcher import TelegramGroupFetcher
import os

def test_group_fetcher_loads_groups():
    test_file = os.path.join(os.path.dirname(__file__), 'resources', 'groups.json')
    fetcher = TelegramGroupFetcher(groups_path=test_file)
    groups = fetcher.load_groups()
    assert "web3hiring" in groups  # replace with your actual test data
    assert "masonsalpha" in groups
