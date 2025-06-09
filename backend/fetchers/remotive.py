import requests

def fetch_remotive(keywords=["python"]):
    jobs = []
    resp = requests.get("https://remotive.io/api/remote-jobs")
    if resp.status_code == 200:
        data = resp.json()
        for job in data.get("jobs", []):
            title = job["title"]
            company = job["company_name"]
            link = job["url"]
            description = job["description"]
            date_posted = job["publication_date"]
            location = job["candidate_required_location"]
            salary = job.get("salary", "")
            if any(kw.lower() in (title + description).lower() for kw in keywords):
                jobs.append({
                    "title": title,
                    "company": company,
                    "link": link,
                    "description": description,
                    "date_posted": date_posted,
                    "location": location,
                    "salary": salary,
                })
    return jobs
