import requests
import feedparser

def fetch_weworkremotely(keywords=["python"]):
    jobs = []
    url = "https://weworkremotely.com/categories/remote-programming-jobs.rss"
    feed = feedparser.parse(requests.get(url).content)
    for entry in feed.entries:
        title = entry.title
        link = entry.link
        description = entry.summary
        date_posted = entry.published if hasattr(entry, "published") else ""
        location = ""
        salary = ""
        if any(kw.lower() in (title + description).lower() for kw in keywords):
            jobs.append({
                "title": title,
                "company": "",
                "link": link,
                "description": description,
                "date_posted": date_posted,
                "location": location,
                "salary": salary,
            })
    return jobs
