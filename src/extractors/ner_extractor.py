# extractors/ner_extractor.py
from transformers import pipeline

# Loads once; re-use for all calls.
ner = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")

def extract_ner_fields(text):
    entities = ner(text)
    company, title, location = "", "", ""
    for ent in entities:
        if ent['entity_group'] == "ORG" and not company:
            company = ent["word"]
        elif ent['entity_group'] == "LOC" and not location:
            location = ent["word"]
        elif ent['entity_group'] == "PER" and not title:
            title = ent["word"]
    return {
        "company": company,
        "title": title,
        "location": location
    }
