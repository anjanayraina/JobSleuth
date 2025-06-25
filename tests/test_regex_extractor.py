import pytest
from extractors.regex_extractor import extract_url, extract_salary

class TestRegexExtractor:
    def test_extract_url_single(self):
        text = "Apply here: https://careers.microsoft.com/job/1234"
        assert extract_url(text) == "https://careers.microsoft.com/job/1234"

    def test_extract_url_none(self):
        text = "No link in this post."
        assert extract_url(text) == None

    def test_extract_salary_range(self):
        text = "Salary: ₹20L–₹35L per annum"
        assert "20L" in extract_salary(text)
        assert "35L" in extract_salary(text)

    def test_extract_salary_none(self):
        text = "No salary mentioned"
        assert extract_salary(text) == None
