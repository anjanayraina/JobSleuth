import re

def extract_url(text):
    url_pattern = re.compile(
        r'(https?://[^\s]+)'
    )
    match = url_pattern.search(text)
    return match.group(1) if match else None

def extract_salary(text):
    salary_pattern = re.compile(r'(\$\d{1,3}(?:[kK]|,?\d{3,})?(\s*-\s*\$\d{1,3}(?:[kK]|,?\d{3,})?)?)')
    match = salary_pattern.search(text)
    return match.group(0) if match else None

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
