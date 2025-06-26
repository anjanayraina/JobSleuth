# extractors/ner_extractor.py
from transformers import pipeline
import re
# You can swap model names here to try different NERs!
ner = pipeline("ner", model="Jean-Baptiste/roberta-large-ner-english", aggregation_strategy="simple")

# Add common job titles for heuristics
COMMON_JOB_TITLES = {
    "engineer", "developer", "manager", "analyst", "consultant",
    "designer", "scientist", "specialist", "intern", "architect",
    "lead", "director", "officer", "administrator", "coordinator",
    "writer", "editor", "product owner"
}

def extract_ner_fields(text):
    # Try regex for title first
    title = extract_title_by_regex(text)
    entities = ner(text)
    company, location = "", ""
    for ent in entities:
        if ent['entity_group'] == "ORG" and not company:
            if ent["word"].lower() not in COMMON_JOB_TITLES and len(ent["word"]) > 2:
                company = ent["word"]
        elif ent['entity_group'] == "LOC" and not location:
            location = ent["word"]
    return {
        "company": company.strip(),
        "title": title.strip(),
        "location": location.strip()
    }

def extract_title_by_regex(text):
    # Common patterns for title
    patterns = [
        r"Position:\s*([^\n]+)",
        r"Role:\s*([^\n]+)",
        r"Job Title:\s*([^\n]+)",
        r"Title:\s*([^\n]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip(" *:–-")
    return ""
