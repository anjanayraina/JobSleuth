import re

def extract_url(text):
    url_pattern = re.compile(
        r'(https?://[^\s]+)'
    )
    match = url_pattern.search(text)
    return match.group(1) if match else None

def extract_salary(text: str) -> str:
    # Remove links from the text before extracting salary
    text_wo_links = re.sub(r'https?://\S+', '', text)

    # Currency symbols/words
    currency = r'(₹|Rs\.?|INR|\$|USD|€|EUR|£|GBP|dollars?|euros?|rupees?)'
    # Number pattern (including commas, dots, decimals)
    number = r'(?:\d{1,3}(?:,\d{3})*|\d+)(?:\.\d+)?'
    # Units (k/K/l/L/m/M/cr/Crore/lakh/million/billion)
    unit = r'(?:[kKlLmM]|lakh|cr|crore|million|billion)'
    # 1. Range pattern (20L–35L, $100k-$120k, etc.)
    range_pattern = (
        rf'({currency}?\s*{number}\s*{unit}?\s*(?:-|–|to)\s*{currency}?\s*{number}\s*{unit}?)'
    )
    # 2. Simple pattern with currency and number/unit (Rs. 50,000, USD 200k, etc.)
    simple_pattern = rf'({currency}\s*{number}\s*{unit}?)'
    # 3. Pattern: number + unit + currency word at end (1.2 million dollars, 12 lakh rupees, etc.)
    end_pattern = rf'({number}\s*{unit}\s*{currency})'
    # 4. Direct number with unit and no explicit currency (e.g., "12 Lakh to 20 Lakh")
    direct_pattern = rf'({number}\s*{unit}\s*(?:-|–|to)\s*{number}\s*{unit})'

    # Combine all patterns
    pattern = f"{range_pattern}|{simple_pattern}|{end_pattern}|{direct_pattern}"

    matches = re.findall(pattern, text_wo_links, re.IGNORECASE)
    # Flatten and clean results
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
    # Telegram username usually like @something (not in emails)
    username_pattern = re.compile(r'@[a-zA-Z0-9_]{5,32}')
    matches = username_pattern.findall(text)
    # Remove if it's part of an email
    return next((u for u in matches if "@" + u[1:] not in text), None)

def extract_special_location_keywords(text):
    """Return 'Remote', 'Hybrid', 'On site', etc. if present in the text."""
    text_lower = text.lower()
    location_keywords = []
    if "remote" in text_lower:
        location_keywords.append("Remote")
    if "hybrid" in text_lower:
        location_keywords.append("Hybrid")
    if "on site" in text_lower or "onsite" in text_lower:
        location_keywords.append("On site")
    return location_keywords
