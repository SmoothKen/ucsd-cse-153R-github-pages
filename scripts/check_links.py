from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

root = Path(__file__).resolve().parents[1]

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.append(href)

links = set()
for path in root.glob("*.html"):
    parser = LinkParser()
    parser.feed(path.read_text())
    for href in parser.links:
        if href.startswith(("http://", "https://")):
            links.add(href)

for url in sorted(links):
    try:
        req = Request(url, method="HEAD", headers={"User-Agent": "course-link-check/1.0"})
        with urlopen(req, timeout=15) as r:
            print(f"{r.status:>3} {url}")
    except HTTPError as e:
        print(f"{e.code:>3} {url}")
    except URLError as e:
        print(f"ERR {url} -- {e.reason}")
