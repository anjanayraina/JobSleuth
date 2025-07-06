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
    # FAANG, MAANG, and big tech
    "google", "facebook", "meta", "apple", "amazon", "microsoft", "netflix",
    "tiktok", "twitter", "x", "openai", "stripe", "uber", "airbnb", "shopify",

    # Other US/EU tech giants
    "linkedin", "youtube", "instagram", "snapchat", "slack", "dropbox", "zoom", "adobe", "oracle", "salesforce",
    "paypal", "square", "block", "coinbase", "robinhood", "github", "gitlab", "asana", "notion", "figma",

    # Cloud/enterprise/AI
    "databricks", "snowflake", "palantir", "huawei", "sap", "ibm", "red hat", "cloudflare", "digitalocean", "fastly",

    # Crypto & web3
    "binance", "coinbase", "kraken", "consensys", "alchemy", "chainlink", "polygon", "solana", "circle", "ripple", "gemini",

    # Indian/Asian unicorns & startups
    "ola", "flipkart", "swiggy", "zomato", "paytm", "inmobi", "freshworks", "browserstack", "razorpay",

    # More SaaS/product/startup companies
    "atlassian", "zendesk", "intercom", "monday.com", "clickup", "miro", "mailchimp", "calendly", "hubspot", "wise",
    "wise", "wise", "wise",
    "klarna", "revolut", "n26", "stripe", "wise", "coinbase", "revolut", "robinhood",

    # Misc
    "bytedance", "plaid", "square", "brex", "expedia", "doordash", "lyft", "grab", "glovo", "deliveroo", "toss"
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
