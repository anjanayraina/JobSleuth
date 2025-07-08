import re
from extractors.regex_extractor import extract_url
from extractors.ner_extractor import extract_ner_fields
from extractors.llm_extractor import extract_with_llm

def extract_title_company_regex(text):
    # Common job patterns (add more as needed!)
    patterns = [
        r"(?i)hiring\s+(?P<title>[\w\s/-]+)\s+at\s+(?P<company>[\w\s&.,-]+)",
        r"(?i)(?P<company>[\w\s&.,-]+)\s+is\s+looking\s+for\s+a[n]?\s+(?P<title>[\w\s/-]+)",
        r"(?i)position:\s*(?P<title>[\w\s/-]+),\s*company:\s*(?P<company>[\w\s&.,-]+)"
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group("title").strip(), match.group("company").strip()
    return "", ""

def extract_job_fields(text, api_key):
    # 1. Extract link with regex
    link = extract_url(text)
    # 2. NER for company/title
    ner_fields = extract_ner_fields(text)
    title, company = ner_fields.get('title', ""), ner_fields.get('company', "")
    # 3. Fallback to regex if NER fails
    if not title or not company:
        regex_title, regex_company = extract_title_company_regex(text)
        title = title or regex_title
        company = company or regex_company
    # 4. Fallback to LLM if still missing
    if (not title or not company) and api_key:
        llm_fields = extract_with_llm(text, api_key)
        title = title or llm_fields.get('title', "")
        company = company or llm_fields.get('company', "")
        link = link or llm_fields.get('link', "")
    # 5. Validate required fields
    if not (title and company and link):
        return None
    # 6. Accept
    return {
        "title": title,
        "company": company,
        "link": link,
        "description": text
        # Optionally add date_posted, location, salary if you want
    }
