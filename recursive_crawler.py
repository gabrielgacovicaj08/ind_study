
from threading import Lock
import requests
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import time
import json


START_URLS= ["https://msutexas.edu/academics/", "https://msutexas.edu/admissions/", "https://msutexas.edu/student-life/", "https://msutexas.edu/distance/", "https://msutexas.edu/finaid/"]
# PATHS = [urlparse(url).path for url in START_URLS]
# DOMAIN = urlparse(START_URL).netloc
# PATH = urlparse(START_URL).path
MAX_DEPTH = 10
MAX_WORKER = 25
documents=[]
visited = set()

lock = Lock()

def clean_html(raw_html):
    """Removes scripts, styles, and extracts readable text."""
    soup = BeautifulSoup(raw_html, "html.parser")
    
    # Remove noisy tags
    for tag in soup(["script", "style", "nav", "footer", "header", "form", "a"]):
        tag.decompose()

    # Extract text
    text = soup.get_text(separator=" ", strip=True)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\x00-\x7F]+", " ", text)
    return text.strip()

def safe_url_visited(url):
    with lock:
        if url in visited:
            return False
        else:
            visited.add(url)
            return True

def safe_doc(doc):
    with lock:
        documents.append(doc)

def crawl(url, DOMAIN, PATH, depth=0):
    
    if not safe_url_visited(url) or depth >= MAX_DEPTH:
        return 
    # visited.add(url)

    try:
        response = requests.get(url)
        if response.status_code != 200 or "text/html" not in response.headers.get("Content-Type", ""):
            return
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return 
    
    print(f"{'  '*depth}→ Crawling: {url}")
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.get_text(strip=True) if soup.title else "No title"

    text = clean_html(response.text)

    if len(text) < 100:
        return 
    
    doc ={
        "page_content": text,
        "metadata": {"url":url, "title":title}
    }

    with open("msu_texas_info_crawler_no_AI.jsonl", "a") as f:
        f.write(json.dumps(doc) + '\n')
    # documents.append(doc)
    safe_doc(doc)

    for link_tag in soup.find_all("a", href = True):
        link = urljoin(url, link_tag["href"])
        parsed_link = urlparse(link)
        if parsed_link.netloc.endswith(DOMAIN) and parsed_link.path.startswith(PATH) and parsed_link.fragment == "":
            crawl(link, DOMAIN, PATH, depth + 1)
            time.sleep(1)



with ThreadPoolExecutor(MAX_WORKER) as executor:
    for url in START_URLS:
        parsed = urlparse(url)
        executor.submit(crawl, url, parsed.netloc, parsed.path)