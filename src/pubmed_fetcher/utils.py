import re
from typing import Optional

def is_biotech_or_pharma(affiliation: str) -> bool:
    affiliation = affiliation.lower()
    company_keywords = [
        "pharma", "biotech", "inc", "llc", "ltd", "gmbh", "s.a.", "s.p.a", "corporation",
        "sanofi", "pfizer", "moderna", "astrazeneca", "novartis", "roche", "merck", "abbvie", "bayer"
    ]
    return any(keyword in affiliation for keyword in company_keywords)

def extract_email(text: str) -> Optional[str]:
    match = re.search(r"[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else None