from typing import List, Dict, Optional
import requests
import xml.etree.ElementTree as ET
from pubmed_fetcher.utils import is_biotech_or_pharma, extract_email

def fetch_pubmed_ids(query: str, debug: bool = False) -> List[str]:
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {"db": "pubmed", "term": query, "retmode": "json", "retmax": "20"}
    if debug:
        print(f"[DEBUG] ESearch URL: {url}?db=pubmed&term={query.replace(' ', '+')}&retmode=json&retmax=20")
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data.get("esearchresult", {}).get("idlist", [])
    except Exception as e:
        print(f"[ERROR] Failed to fetch PubMed IDs: {e}")
        return []

def parse_article(article: ET.Element, debug: bool = False) -> Optional[Dict[str, Optional[str]]]:
    try:
        pmid = article.findtext("MedlineCitation/PMID")
        title = article.findtext("MedlineCitation/Article/ArticleTitle")
        pub_year = article.findtext("MedlineCitation/Article/Journal/JournalIssue/PubDate/Year") or "N/A"

        authors_el = article.findall(".//Author")
        non_academic_authors = []
        company_affiliations = []
        corresponding_email = "N/A"

        for author in authors_el:
            last = author.findtext("LastName") or ""
            fore = author.findtext("ForeName") or ""
            name = f"{fore} {last}".strip()

            aff_el = author.find("AffiliationInfo")
            affiliation = aff_el.findtext("Affiliation") if aff_el is not None else ""

            if debug:
                print(f"[DEBUG] Author: {name}, Affiliation: {affiliation}")

            if is_biotech_or_pharma(affiliation):
                non_academic_authors.append(name)
                company_affiliations.append(affiliation)
                if corresponding_email == "N/A":
                    email = extract_email(affiliation)
                    if email:
                        corresponding_email = email

        return {
            "PubmedID": pmid,
            "Title": title,
            "Publication Date": pub_year,
            "Non-academicAuthor(s)": "; ".join(non_academic_authors),
            "CompanyAffiliation(s)": "; ".join(company_affiliations),
            "Corresponding Author Email": corresponding_email,
        }
    except Exception as e:
        if debug:
            print(f"[ERROR] Failed to parse article: {e}")
        return None

def fetch_papers(query: str, debug: bool = False) -> List[Dict[str, Optional[str]]]:
    id_list = fetch_pubmed_ids(query, debug)
    if not id_list:
        return []

    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    try:
        ids = ",".join(id_list)
        params = {"db": "pubmed", "id": ids, "retmode": "xml"}
        if debug:
            print(f"[DEBUG] EFetch URL: {url}?db=pubmed&id={ids}&retmode=xml")

        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        root = ET.fromstring(resp.content)

        results = []
        for article in root.findall(".//PubmedArticle"):
            paper = parse_article(article, debug)
            if paper:
                if debug:
                    print(f"[DEBUG] Paper PMID: {paper['PubmedID']}, Title: {paper['Title']}")
                results.append(paper)
        return results
    except Exception as e:
        print(f"[ERROR] Failed to fetch paper details: {e}")
        return []