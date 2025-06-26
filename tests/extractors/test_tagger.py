import pytest
from extractors.tagger import extract_tags

class TestTagger:
    def test_extract_tech_tags(self):
        desc = "We are looking for Python and React developers with experience in AWS and Docker."
        tags = extract_tags(desc)
        assert "python" in tags
        assert "react" in tags
        assert "aws" in tags
        assert "docker" in tags

    def test_extract_industry_tags(self):
        desc = "Join a dynamic fintech startup working on decentralized finance and blockchain!"
        tags = extract_tags(desc)
        assert "fintech" in tags or "blockchain" in tags

    def test_extract_multiple_tags(self):
        desc = "Skills: JavaScript, Node.js, Cloud, SaaS, Machine Learning"
        tags = extract_tags(desc)
        assert "javascript" in tags
        assert "cloud" in tags
        assert "machine learning" in tags

    def test_extract_tags_none(self):
        desc = "No technical or industry keywords."
        tags = extract_tags(desc)
        assert tags == []
