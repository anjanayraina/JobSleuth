import re

def extract_url(text):
    url_pattern = re.compile(
        r'(https?://[^\s]+)'
    )
    match = url_pattern.search(text)
    return match.group(1) if match else None

def extract_salary(text: str) -> str:
    # Currency symbols/words
    currency = r'(₹|Rs\.?|INR|\$|USD|€|EUR|£|GBP|dollars?|euros?|rupees?)'
    # Number pattern (including commas, dots, etc.)
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
    # Combine all patterns
    pattern = f"{range_pattern}|{simple_pattern}|{end_pattern}"

    matches = re.findall(pattern, text, re.IGNORECASE)
    # Flatten and clean results
    results = []
    for groups in matches:
        # The matched group is always in the first group with value
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
