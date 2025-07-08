import re
from extractors.constants import TECH_TAGS,INDUSTRY_TAGS,COMPANY_TAGS



def extract_tags(text):
    text_lower = text.lower()
    tags = set()

    # Tech tags
    for tag in TECH_TAGS:
        if re.search(rf"\b{re.escape(tag)}\b", text_lower):
            tags.add(tag)

    # Industry tags
    for tag, keywords in INDUSTRY_TAGS:
        for keyword in keywords:
            if re.search(rf"\b{re.escape(keyword)}\b", text_lower):
                tags.add(tag)
                break

    # Big company tags
    for tag in COMPANY_TAGS:
        if re.search(rf"\b{re.escape(tag)}\b", text_lower):
            tags.add(tag)

    return list(tags)
