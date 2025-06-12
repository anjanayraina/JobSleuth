# ✅ Job Search Automation Tool — Feature Tracker

This file documents all current, planned, and potential features for the Job Search Automation Tool.

---

## 🧩 1. Job Fetchers (Core Sources)

| Source         | Status       | Method         | Notes                          |
|----------------|--------------|----------------|---------------------------------|
| RemoteOK       | ✅ Done       | RSS/API        | Stable, reliable               |
| WeWorkRemotely | ✅ Done       | RSS            | Dev-focused                    |
| Remotive       | ✅ Done       | Public API     | Clean JSON                     |
| Crypto.jobs    | ✅ Done       | HTML           | Simple card parsing            |
| Greenhouse     | 🛠 In Progress| JSON API       | Used by 100s of startups       |
| Lever          | 🛠 In Progress| JSON API       | Easy job listing endpoint      |
| Python.org     | 🔄 Planned    | RSS            | Dev-specific jobs              |
| Jobspresso     | 🔄 Planned    | HTML/RSS       | Remote-friendly                |
| Internshala    | 🔄 Planned    | HTML Scraping  | India-focused internships      |
| Wellfound      | ❌ Dropped    | React-heavy    | API not public                 |
| Glassdoor      | ⚠️ Difficult  | JS + Cloudflare| Consider if headless browser   |
| LinkedIn       | ❌ Blocked    | API forbidden  | Risky scraping                 |

---

## 🔥 2. Social & Community Sources

| Platform    | Status       | Method         | Notes                             |
|-------------|--------------|----------------|------------------------------------|
| Twitter (X) | ✅ To Do      | snscrape       | Hashtag & keyword-based scraping  |
| Telegram    | ✅ To Do      | Telethon       | Public channel parsing            |
| HN (Hiring) | 🔄 Planned    | HTML Thread    | Parse monthly "Who is hiring"     |
| Reddit      | Optional     | HTML           | r/forhire, r/RemoteWork, etc.     |

---

## 📚 3. Metadata & Application Enhancers

- [ ] Keyword-based job scoring system
- [ ] Resume match % calculator
- [ ] LLM-based Cover Letter Generator (OpenAI)
- [ ] LinkedIn people finder for jobs (outreach targets)
- [ ] Outreach automation templates (email / DM)
- [ ] Follow-up reminders via Telegram/Email
- [ ] Notes & contact logging for each job

---

## 📊 4. Analytics (Optional Phase)

- [ ] Application count / conversion stats
- [ ] Job source efficiency breakdown
- [ ] Charts: Jobs/week, replies, interviews, etc.

---

## 🧪 5. Tech Stack & Deployment

- [x] FastAPI backend for endpoints
- [ ] React frontend with filters and job list
- [ ] CLI interface for quick usage
- [ ] SQLite or Airtable job tracker
- [ ] Docker setup for deployment
- [ ] Configurable `settings.json` for preferences

---

_Last updated: 2025-06-09_
