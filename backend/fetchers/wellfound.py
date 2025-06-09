import requests

def fetch_wellfound(keywords=["python"]):
    jobs = []
    for kw in keywords:
        url = f"https://wellfound.com/jobs/api/v1/jobs"
        params = {
            "query": kw,
            "remote": "true",
            "page": 1,
            "sort": "recent"
        }
        resp = requests.get(url, params=params, headers={"User-Agent": "Mozilla/5.0"})
        if resp.status_code == 200:
            data = resp.json()
            for job in data.get("jobs", []):
                jobs.append({
                    "title": job.get("title"),
                    "company": job.get("company", {}).get("name"),
                    "link": f"https://wellfound.com/jobs/{job.get('id')}",
                    "description": job.get("description", ""),
                    "date_posted": job.get("published_at"),
                    "location": job.get("location", "Remote"),
                    "salary": job.get("salary_range", ""),
                })
    return jobs
