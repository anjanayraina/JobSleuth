import pytest
from extractors.llm_extractor import extract_with_llm
from helper.config import ConfigSingleton

class TestLLMExtractor:
    def setup_method(self):
        self.config = ConfigSingleton()
        self.api_key = self.config.openrouter_api_key
        if not self.api_key:
            pytest.skip("OPEN_ROUTER_KEY not set in environment or .env file")

    def test_extract_with_llm_simple(self):
        text = (
            "Google is hiring a Backend Engineer!\n"
            "Location: Mountain View, CA\n"
            "Apply here: https://google.com/careers/job/123"
        )
        result = extract_with_llm(text, self.api_key)
        assert isinstance(result, dict)
        assert result["company"].lower() == "google"
        assert "engineer" in result["title"].lower()
        assert "mountain view" in result["location"].lower() or "ca" in result["location"].lower()

    def test_extract_with_llm_complex(self):
        text = (
            "Join Meta as a Senior AI/ML Researcher. Position in New York, remote possible. "
            "Email your resume to jobs@meta.com."
        )
        result = extract_with_llm(text, self.api_key)
        assert "researcher" in result["title"].lower() or "ai/ml" in result["title"].lower()
        assert "new york" in result["location"].lower() or "remote" in result["location"].lower()

    def test_extract_with_llm_edge_case(self):
        text = (
            "We're looking for a Frontend Wizard to join the Titan team, fully remote."
            " No links included in this message."
        )
        result = extract_with_llm(text, self.api_key)
        assert "titan" in result["company"].lower()
        assert "frontend" in result["title"].lower()
        assert "remote" in result["location"].lower()

    def test_extract_with_llm_no_company(self):
        text = (
            "Hiring: Python Developer, work from anywhere. Salary: $120k. "
            "Apply at jobs@pythondev.com"
        )
        result = extract_with_llm(text, self.api_key)
        # May not find a company, so just check the others
        assert "python" in result["title"].lower()
        assert "developer" in result["title"].lower()
        assert isinstance(result["company"], str)
    def test_extraction_invalid_job(self):
        text = "Hello, how are you? Just a random message."
        result = extract_with_llm(text, self.api_key)
        assert result["company"] in ["", "NA", "N/A"]
        assert result["title"] in ["", "NA", "N/A"]
