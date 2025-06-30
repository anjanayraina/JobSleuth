import requests

def extract_with_llm(text, api_key):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
    }
    prompt = (
        "Extract the company, job title, and location from the following job posting. "
        "Respond ONLY as JSON with keys 'company', 'title', and 'location'.\n\n"
        f"{text}"
    )
    data = {
        "model": "mistralai/mistral-7b-instruct",  # or try another model if needed
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=20)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        # Try parsing output as JSON
        import json
        fields = json.loads(content)
        # fallback in case keys missing
        return {
            "company": fields.get("company", ""),
            "title": fields.get("title", ""),
            "location": fields.get("location", "")
        }
    except Exception as e:
        # Fallback: return empty fields on any error
        print(f"LLM extraction failed: {e}")
        return {"company": "", "title": "", "location": ""}
