# extractors/regex_extractor.py
import re

def extract_url(text):
    match = re.search(r'https?://\S+', text)
    return match.group() if match else ""

def extract_salary(text):
    match = re.search(r'(\$|₹|€|£)\s?[\d,]+(\s?-\s?(\$|₹|€|£)?[\d,]+)?', text)
    return match.group() if match else ""

def extract_date(text):
    # Placeholder: could use dateparser or similar lib
    return ""

