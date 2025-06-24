import re

def extract_url(text):
    urls = re.findall(r'(https?://[^\s]+)', text)
    return urls[0] if urls else ""

def extract_salary(text):
    match = re.search(r'(\$\d{1,3}(?:,\d{3})*(?:k)?(?:-\$?\d{1,3}(?:,\d{3})*(?:k)?)?)', text, re.I)
    return match.group(1) if match else ""
