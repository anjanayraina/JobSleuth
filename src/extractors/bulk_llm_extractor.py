import requests
import json
from helper.logger import Logger

log = Logger(__name__)


def extract_jobs_with_bulk_llm(api_key: str, texts: list[str]) -> list:

    if not texts:
        return []

    url = "https://ai-marketplace-iypm.onrender.com/LLM/bulk-prompt-to-json"

    data = {
        "apiKey": api_key,
        "modelName": "openai/gpt-oss-120b",
        "temperatureValue": 0,
        "prompts": texts,
        "responseStruct": [
            {
                "fieldName": "title",
                "fieldDtype": "str",
                "fieldDescription": "Job title (e.g., “Compliance Analyst , Software Developer”)",
                "nullable": False,
                "required": True,
            },
            {
                "fieldName": "company",
                "fieldDtype": "str",
                "fieldDescription": "Hiring company name",
                "nullable": False,
                "required": True,

            },
            {
                "fieldName": "location",
                "fieldDtype": "str",
                "fieldDescription": "Job location (city, country) or empty string if unknown",
                "nullable": True,
                "required": False,

            },
            {
                "fieldName": "salary",
                "fieldDtype": "str",
                "fieldDescription": "Salary range text or empty string if not provided",
                "nullable": True,
                "required": False
            },
            {
                "fieldName": "link",
                "fieldDtype": "str",
                "fieldDescription": "Direct URL to the job posting",
                "nullable": True,
                "required": False,

            },
            {
                "fieldName": "description",
                "fieldDtype": "str",
                "fieldDescription": "A brief description of the job posting",
                "nullable": True,
                "required": False,
            },

            {
                "fieldName": "contact",
                "fieldDtype": "str",
                "fieldDescription": "Recruiter email or profile link if available",
                "nullable": True,
                "required": False,

            },
            {
                "fieldName": "tags",
                "fieldDtype": "List<str>",
                "fieldDescription": "Keywords from the job postings that can be used for searching the job postings",
                "nullable": True,
                "required": False,

            }
        ]
    }

    try:
        log.info(f"Sending {len(texts)} job postings to bulk LLM service...")
        print(f"Request Body : {data}")
        response = requests.post(url, json=data, timeout=300)
        response.raise_for_status()

        extracted_data = response.json()
        log.info(f"Successfully received {len(extracted_data)} results from LLM.")
        return extracted_data

    except requests.exceptions.HTTPError as http_err:
        log.error(f"HTTP error during bulk LLM call: {http_err}")
        log.error(f"Response body: {response.text}")
    except Exception as e:
        log.error(f"An error occurred during bulk LLM call: {e}")

    return []