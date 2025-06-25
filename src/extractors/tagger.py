import re

TECH_TAGS = [
    "python", "java", "solidity", "javascript", "typescript", "react", "node",
    "spring", "quarkus", "intellij", "git", "svn", "django", "flask", "aws",
    "azure", "docker", "kubernetes", "tensorflow", "pytorch"
]
INDUSTRY_TAGS = [
    ("crypto", ["crypto", "blockchain", "web3", "defi", "token"]),
    ("ai/ml", ["ai", "artificial intelligence", "ml", "machine learning", "deep learning", "data science"]),
    ("cloud", ["cloud", "aws", "azure", "gcp", "google cloud", "cloud computing"]),
    ("software development", ["developer", "programming", "engineer", "software", "application"]),
    ("fintech", ["fintech", "finance", "bank", "trading", "payments"]),
    ("data science", ["data science", "data analyst", "big data", "analytics", "data engineer"]),
]

def extract_tags(text):
    text_lower = text.lower()
    tags = set()
    for tag in TECH_TAGS:
        if re.search(rf"\b{re.escape(tag)}\b", text_lower):
            tags.add(tag)
    for tag, keywords in INDUSTRY_TAGS:
        for keyword in keywords:
            if re.search(rf"\b{re.escape(keyword)}\b", text_lower):
                tags.add(tag)
                break
    return list(tags)
