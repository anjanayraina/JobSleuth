import re

TECH_TAGS = [
    "python", "java", "solidity", "javascript", "typescript", "react", "node",
    "spring", "quarkus", "intellij", "git", "svn", "django", "flask", "aws",
    "azure", "docker", "kubernetes", "tensorflow", "pytorch", "go", "golang",
    "rust", "scala", "c++", "c#", ".net", "php", "swift", "kotlin", "sql",
    "nosql", "mysql", "postgresql", "mongodb", "redis", "graphql", "rest",
    "grpc", "firebase", "gcp", "google cloud", "html", "css", "sass", "tailwind",
    "bootstrap", "vue", "angular", "redux", "storybook", "express", "lambda",
    "terraform", "ansible", "jenkins", "jira", "airflow"
]

INDUSTRY_TAGS = [
    ("crypto", ["crypto", "blockchain", "web3", "defi", "token", "nft", "dao"]),
    ("ai/ml", ["ai", "artificial intelligence", "ml", "machine learning", "deep learning", "data science", "nlp", "natural language", "computer vision", "llm"]),
    ("cloud", ["cloud", "aws", "azure", "gcp", "google cloud", "cloud computing", "serverless", "saas", "paas", "iaas"]),
    ("software development", ["developer", "programming", "engineer", "software", "application", "devops", "sre"]),
    ("fintech", ["fintech", "finance", "bank", "trading", "payments", "investment", "wallet", "remittance"]),
    ("data science", ["data science", "data analyst", "big data", "analytics", "data engineer", "bi", "etl", "data pipeline"]),
    ("ecommerce", ["ecommerce", "e-commerce", "retail", "shopping", "marketplace"]),
    ("healthtech", ["healthtech", "health care", "medical", "medtech", "pharma", "biotech", "life sciences"]),
    ("edtech", ["edtech", "education", "learning", "edtech platform"]),
    ("insuretech", ["insuretech", "insurance", "policy", "claims"]),
    ("gaming", ["gaming", "game development", "esports"]),
    ("telecom", ["telecom", "telecommunications", "5g", "networking"]),
    ("media", ["media", "video", "content", "broadcast", "streaming"]),
]

COMPANY_TAGS = [
    # Not for company extraction! Just if you want to tag "FAANG" or major employers as a tech stack/category
    "google", "facebook", "meta", "apple", "amazon", "microsoft", "netflix", "tiktok", "twitter", "x", "openai", "stripe", "uber", "airbnb", "shopify"
]

def extract_tags(text):
    text_lower = text.lower()
    tags = set()

    # Tech tags
    for tag in TECH_TAGS:
        if re.search(rf"\b{re.escape(tag)}\b", text_lower):
            tags.add(tag)

    # Industry tags
    for tag, keywords in INDUSTRY_TAGS:
        for keyword in keywords:
            if re.search(rf"\b{re.escape(keyword)}\b", text_lower):
                tags.add(tag)
                break

    # Big company tags
    for tag in COMPANY_TAGS:
        if re.search(rf"\b{re.escape(tag)}\b", text_lower):
            tags.add(tag)

    return list(tags)
