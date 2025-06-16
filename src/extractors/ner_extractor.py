# extractors/ner_extractor.py
from transformers import pipeline

# You can swap model names here to try different NERs!
ner = pipeline("ner", model="Jean-Baptiste/roberta-large-ner-english", aggregation_strategy="simple")

# Add common job titles for heuristics
COMMON_JOB_TITLES = {
    "engineer", "developer", "manager", "analyst", "consultant",
    "designer", "scientist", "specialist", "intern", "architect",
    "lead", "director", "officer", "administrator", "coordinator",
    "writer", "editor", "product owner"
}

def extract_ner_fields(text):
    entities = ner(text)
    company, title, location = "", "", ""
    for ent in entities:
        if ent['entity_group'] == "ORG" and not company:
            # Ignore short ORGs that are job titles
            if ent["word"].lower() not in COMMON_JOB_TITLES and len(ent["word"]) > 2:
                company = ent["word"]
        elif ent['entity_group'] in ("PER", "MISC") and not title:
            # Accept any reasonable title
            if 3 <= len(ent["word"].split()) <= 8:
                title = ent["word"]
        elif ent['entity_group'] == "LOC" and not location:
            location = ent["word"]
    return {
        "company": company.strip(),
        "title": title.strip(),
        "location": location.strip()
    }
