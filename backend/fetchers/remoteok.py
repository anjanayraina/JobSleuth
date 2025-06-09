import re
import requests
from bs4 import BeautifulSoup
import re

def extract_salary_from_text(text):
    """
    Extract salary or salary range from text.
    Examples matched:
      "$65k–$120k", "$65,000-$120,000", "$65k-$120k", "$100k", "$65k+", etc.
    """
    # Regex for a range, e.g. "$65k–$120k" or "$65,000-$120,000"
    range_pattern = re.compile(
        r"\$\s?(\d{2,3}(?:[,.]?\d{3})?[kK]?)\s*[-–to]+\s*\$\s?(\d{2,3}(?:[,.]?\d{3})?[kK]?)",
        re.IGNORECASE
    )
    # Regex for a single value, e.g. "$100k" or "$65,000"
    single_pattern = re.compile(
        r"\$\s?(\d{2,3}(?:[,.]?\d{3})?[kK]?)(?:\+)?",
        re.IGNORECASE
    )
    # Try to find a range first
    match = range_pattern.search(text)
    if match:
        return f"${match.group(1)}–${match.group(2)}"
    # Otherwise, find first single value
    match = single_pattern.search(text)
    if match:
        return f"${match.group(1)}"
    return ""


def fetch_remoteok(keywords=["python"]):
    jobs = []
    for kw in keywords:
        url = f"https://remoteok.com/remote-{kw}-jobs"
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        job_rows = soup.find_all("tr", class_="job")
        for row in job_rows:
            try:
                title = row.find("h2", itemprop="title").get_text(strip=True)
                company = row.find("h3", itemprop="name").get_text(strip=True)
                link = "https://remoteok.com" + row['data-href']
                desc = row.get('data-tags', '')
                description_text = row.text
                date_posted = row.find("time")
                date_posted = date_posted["datetime"] if date_posted else ""
                location = row.find("div", class_="location")
                location = location.get_text(strip=True) if location else "Remote"
                salary = row.find("div", class_="salary")
                salary = salary.get_text(strip=True) if salary else extract_salary_from_text(description_text)
                jobs.append({
                    "title": title,
                    "company": company,
                    "link": link,
                    "description": desc,
                    "date_posted": date_posted,
                    "location": location,
                    "salary": salary,
                })
            except Exception:
                continue
    return jobs
