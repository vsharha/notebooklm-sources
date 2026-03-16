import itertools

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re


def glob_to_regex(pattern: str) -> re.Pattern:
    regex = re.escape(pattern)
    regex = regex.replace(r"\*", "[^/]+")
    return re.compile("^" + regex + "$")


def same_domain(base: str, url: str) -> bool:
    return urlparse(base).netloc == urlparse(url).netloc


def collect_links(page_url: str, path_pattern: str) -> set[str]:
    rx = glob_to_regex(path_pattern)

    html = requests.get(page_url).text
    soup = BeautifulSoup(html, "html.parser")

    matches = set()

    for a in soup.select("a[href]"):
        href = urljoin(page_url, a["href"])

        if urlparse(href).netloc != urlparse(page_url).netloc:
            continue

        path = urlparse(href).path.lstrip("/")

        # Absolute path pattern
        if path_pattern.startswith("/"):
            if rx.match("/" + path):
                matches.add(href)
        # Relative (suffix) pattern
        else:
            if rx.match(path.split("/")[-1]):
                matches.add(href)

    return matches


def collect_indexed_pages(base_url: str, pattern: str) -> set[str]:
    pages = set()
    for i in itertools.count(1):
        url = urljoin(base_url.rstrip("/") + "/", pattern.replace("{n}", str(i)))
        resp = requests.get(url)
        if resp.status_code != 200:
            break
        pages.add(url)
    return pages
