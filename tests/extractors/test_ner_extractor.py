import pytest
from extractors.ner_extractor import extract_ner_fields

class TestNERExtractor:
    def test_extract_ner_company_title_location(self):
        text = "Amazon Web Services (AWS) is hiring!\nPosition: Senior Cloud Architect\nLocation: Bengaluru, India"
        result = extract_ner_fields(text)
        assert "Amazon" in result["company"] or "Amazon Web Services" in result["company"]
        assert "Cloud Architect" in result["title"] or "Senior Cloud Architect" in result["title"]
        assert "Bengaluru" in result["location"] or "India" in result["location"]

    def test_extract_ner_only_title(self):
        text = "Position: Frontend Developer"
        result = extract_ner_fields(text)
        assert "Frontend Developer" in result["title"]

    def test_extract_ner_empty(self):
        text = "This is a message with no job info."
        result = extract_ner_fields(text)
        assert result["company"] == ""
        assert result["title"] == ""
        assert result["location"] == ""
