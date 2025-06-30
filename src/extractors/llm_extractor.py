import requests
import json

def extract_with_llm(text, api_key):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
    }
    prompt = (
        "Extract the company, job title, and location from the following job posting. "
        "Respond ONLY as JSON with keys 'company', 'title', and 'location'. "
        "If any field cannot be found, set it to \"NA\".\n\n"
        f"{text}"
    )
    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=20)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        try:
            fields = json.loads(content)
        except Exception:
            fields = {"company": "", "title": "", "location": ""}
        # Normalize NA/empty values
        return {
            "company": fields.get("company", "").strip() if fields.get("company", "").strip().lower() not in ["na", "n/a"] else "",
            "title": fields.get("title", "").strip() if fields.get("title", "").strip().lower() not in ["na", "n/a"] else "",
            "location": fields.get("location", "").strip() if fields.get("location", "").strip().lower() not in ["na", "n/a"] else ""
        }
    except Exception as e:
        print(f"LLM extraction failed: {e}")
        return {"company": "", "title": "", "location": ""}
