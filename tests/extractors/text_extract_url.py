# tests/test_url_extractor.py

import pytest
from extractors.regex_extractor import extract_url

class TestURLExtractor:
    def test_single_http_url(self):
        text = "Apply here: http://jobs.example.com/123"
        assert extract_url(text) == "http://jobs.example.com/123"

    def test_single_https_url(self):
        text = "Application link: https://company.com/careers/job456"
        assert extract_url(text) == "https://company.com/careers/job456"

    def test_url_with_query_params(self):
        text = "See details: https://jobs.co/apply?id=789&ref=telegram"
        assert extract_url(text) == "https://jobs.co/apply?id=789&ref=telegram"

    def test_url_with_trailing_slash(self):
        text = "More info at https://startup.io/"
        assert extract_url(text) == "https://startup.io/"

    def test_multiple_urls(self):
        text = "Info at https://first.com and apply at https://second.com/jobs"
        result = extract_url(text)
        assert result in ["https://first.com", "https://second.com/jobs"]  # Accept either if your function returns the first found

    def test_embedded_url(self):
        text = "Check out <a href='https://embedded.com/job'>this job</a>."
        assert "https://embedded.com/job" in extract_url(text)

    def test_no_url(self):
        text = "There is no link in this message."
        assert extract_url(text) == None

    def test_url_with_special_characters(self):
        text = "Apply now: https://example.com/jobs/software-engineer?utm_source=telegram"
        assert extract_url(text) == "https://example.com/jobs/software-engineer?utm_source=telegram"

    def test_url_with_port(self):
        text = "Development server: http://localhost:8080/job/123"
        assert extract_url(text) == "http://localhost:8080/job/123"
