import re

def extract_url(text):
    url_pattern = re.compile(
        r'(https?://[^\s]+)'
    )
    match = url_pattern.search(text)
    return match.group(1) if match else None

def extract_salary(text: str) -> str:
    text_wo_links = re.sub(r'https?://\S+', '', text)

    currency = r'(₹|Rs\.?|INR|\$|USD|€|EUR|£|GBP|dollars?|euros?|rupees?)'
    number = r'(?:\d{1,3}(?:,\d{3})*|\d+)(?:\.\d+)?'
    unit = r'(?:[kKlLmM]|lakh|cr|crore|million|billion)'
    range_pattern = (
        rf'({currency}?\s*{number}\s*{unit}?\s*(?:-|–|to)\s*{currency}?\s*{number}\s*{unit}?)'
    )
    simple_pattern = rf'({currency}\s*{number}\s*{unit}?)'
    end_pattern = rf'({number}\s*{unit}\s*{currency})'
    direct_pattern = rf'({number}\s*{unit}\s*(?:-|–|to)\s*{number}\s*{unit})'

    pattern = f"{range_pattern}|{simple_pattern}|{end_pattern}|{direct_pattern}"

    matches = re.findall(pattern, text_wo_links, re.IGNORECASE)
    results = []
    for groups in matches:
        match = next((g for g in groups if g), "")
        if match:
            results.append(re.sub(r'\s+', ' ', match.strip()))
    return ', '.join(results) if results else ""

def extract_email(text):
    email_pattern = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
    match = email_pattern.search(text)
    return match.group(0) if match else None

def extract_telegram_username(text):
    username_pattern = re.compile(r'@[a-zA-Z0-9_]{5,32}')
    matches = username_pattern.findall(text)
    return next((u for u in matches if "@" + u[1:] not in text), None)

def extract_special_location_keywords(text):
    text_lower = text.lower()
    location_keywords = []
    if "remote" in text_lower:
        location_keywords.append("Remote")
    if "hybrid" in text_lower:
        location_keywords.append("Hybrid")
    if "on site" in text_lower or "onsite" in text_lower:
        location_keywords.append("On site")
    return location_keywords
