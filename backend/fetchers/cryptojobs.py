import requests
from bs4 import BeautifulSoup

def fetch_crypto_jobs(keywords=["python"]):
    jobs = []
    url = "https://crypto.jobs"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    for row in soup.find_all("div", class_="job"):
        title_tag = row.find("h2")
        company_tag = row.find("div", class_="company-name")
        link_tag = row.find("a", href=True)
        desc_tag = row.find("div", class_="description")
        title = title_tag.text.strip() if title_tag else ""
        company = company_tag.text.strip() if company_tag else ""
        link = f"https://crypto.jobs{link_tag['href']}" if link_tag else ""
        description = desc_tag.text.strip() if desc_tag else ""
        if any(kw.lower() in (title + description).lower() for kw in keywords):
            jobs.append({
                "title": title,
                "company": company,
                "link": link,
                "description": description,
                "date_posted": "",
                "location": "",
                "salary": "",
            })
    return jobs
