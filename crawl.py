import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def count_unique_pages(base_url, max_pages=500):
    print(f"Starting crawl of {base_url}")
    queue = [base_url]
    visited = set()
    domain = urlparse(base_url).netloc
    print(f"Domain to crawl: {domain}")
    last_count = 0

    while queue and len(visited) < max_pages:
        url = queue.pop(0)
        if url in visited:
            continue
        print(f"Trying to fetch: {url}")
        try:
            response = requests.get(url, timeout=5)
            if "text/html" not in response.headers.get("Content-Type", ""):
                print(f"Skipping non-HTML content type: {response.headers.get('Content-Type', '')}")
                continue  # skip non-HTML files
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")
            continue

        visited.add(url)
        soup = BeautifulSoup(response.text, "html.parser")

        for link in soup.find_all("a", href=True):
            normalized = urljoin(url, link["href"]).split("#")[0].rstrip("/")
            parsed = urlparse(normalized)
            if parsed.netloc == domain and normalized not in visited:
                queue.append(normalized)
        
        # Print progress when we've found 10 new pages
        if len(visited) - last_count >= 10:
            print(f"Found {len(visited)} unique pages so far...")
            last_count = len(visited)

    return visited


if __name__ == "__main__":
    start_url = "https://www.worldfinancialgroup.com/"
    pages = count_unique_pages(start_url, max_pages=200)
    print(f"Discovered {len(pages)} unique HTML pages:")
    for p in pages:
        print(p)
