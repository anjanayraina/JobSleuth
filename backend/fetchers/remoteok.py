import requests
from bs4 import BeautifulSoup

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
                date_posted = row.find("time")
                date_posted = date_posted["datetime"] if date_posted else ""
                location = row.find("div", class_="location")
                location = location.get_text(strip=True) if location else "Remote"
                salary = row.find("div", class_="salary")
                salary = salary.get_text(strip=True) if salary else ""
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
