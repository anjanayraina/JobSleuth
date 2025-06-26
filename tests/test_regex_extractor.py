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
    def test_extract_salary_range_inr(self):
        text = "Salary: ₹20L–₹35L per annum"
        result = extract_salary(text)
        assert "20L" in result
        assert "35L" in result

    def test_extract_salary_usd_range(self):
        text = "Compensation: $120,000-$150,000"
        result = extract_salary(text)
        assert "$120,000-$150,000" in result

    def test_extract_salary_eur_range(self):
        text = "Annual pay: €70,000 – €90,000 gross"
        result = extract_salary(text)
        assert "€70,000 – €90,000" in result

    def test_extract_salary_gbp_single(self):
        text = "Offer: GBP 60k per year"
        result = extract_salary(text)
        assert "GBP 60k" in result

    def test_extract_salary_inr_monthly(self):
        text = "Monthly: Rs. 50,000"
        result = extract_salary(text)
        assert "Rs. 50,000" in result

    def test_extract_salary_inr_to_range(self):
        text = "CTC: INR 10L to INR 20L"
        result = extract_salary(text)
        assert "INR 10L to INR 20L" in result

    def test_extract_salary_cr(self):
        text = "Salary package: 1cr - 1.5cr"
        result = extract_salary(text)
        assert "1cr - 1.5cr" in result

    def test_extract_salary_million(self):
        text = "Compensation: 1.2 million dollars"
        result = extract_salary(text)
        assert "1.2 million" in result

    def test_extract_salary_k(self):
        text = "USD 200k annual salary"
        result = extract_salary(text)
        assert "USD 200k" in result

    def test_extract_salary_none(self):
        text = "No salary info given here."
        result = extract_salary(text)
        assert result == ""