import fnmatch
import hashlib
import io
import re
import zipfile
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pathlib import Path

COURSES_DIR = "courses"

# Leading bytes of each format, used to reject HTML error pages served with a 200.
_SIGNATURES = {
    ".pdf": b"%PDF",
    ".pptx": b"PK",
    ".docx": b"PK",
}


def normalize_docx(content: bytes) -> bytes:
    """Rename a .docx main part from word/documentN.xml to word/document.xml.

    Word accepts any main part name the package relationships point to, but
    NotebookLM fails to process a .docx whose main part is not word/document.xml.
    """
    with zipfile.ZipFile(io.BytesIO(content)) as src:
        names = src.namelist()
        if "word/document.xml" in names:
            return content
        main = next((n for n in names if re.fullmatch(r"word/document\d+\.xml", n)), None)
        if main is None:
            return content

        stem = Path(main).name
        renames = {main: "word/document.xml", f"word/_rels/{stem}.rels": "word/_rels/document.xml.rels"}
        out = io.BytesIO()
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as dst:
            for name in names:
                data = src.read(name)
                if name in ("_rels/.rels", "[Content_Types].xml"):
                    data = data.replace(main.encode(), b"word/document.xml")
                dst.writestr(renames.get(name, name), data)
    return out.getvalue()


def unique_name(name: str, claimed: set[str]) -> str:
    stem, suffix = Path(name).stem, Path(name).suffix
    candidate = name
    i = 1
    while candidate in claimed:
        candidate = f"{stem}_{i}{suffix}"
        i += 1
    claimed.add(candidate)
    return candidate


def download_files_from_pages(
    pages: set[str],
    subdir: str = "",
    file_types: list[str] | None = None,
    exclude_files: list[str] | None = None,
):
    out = Path(COURSES_DIR) / subdir / "scraped"
    out.mkdir(parents=True, exist_ok=True)
    (Path(COURSES_DIR) / subdir / "manual").mkdir(parents=True, exist_ok=True)

    extensions = {f".{t.lower().lstrip('.')}" for t in (file_types or ["pdf"])}
    existing = {p.name for p in out.iterdir() if p.is_file()}
    # The same file is sometimes linked from several URLs.
    hashes = {hashlib.sha256(p.read_bytes()).digest(): p.name for p in out.iterdir() if p.is_file()}

    seen = set()
    # Different URLs can end in the same filename; pages are visited in a fixed
    # order so the suffixed names stay stable between runs.
    claimed = set()
    skipped = 0
    for page in sorted(pages):
        try:
            html = requests.get(page, timeout=15, headers={"User-Agent": "Mozilla/5.0"}).text
        except requests.exceptions.Timeout:
            print(f"Timed out fetching page: {page}")
            continue
        soup = BeautifulSoup(html, "html.parser")

        for a in soup.select("a[href]"):
            file_url = urljoin(page, a["href"])
            suffix = Path(urlparse(file_url).path).suffix.lower()

            if suffix not in extensions or file_url in seen:
                continue

            seen.add(file_url)
            url_name = Path(urlparse(file_url).path).name

            if exclude_files and any(fnmatch.fnmatch(url_name, pat) for pat in exclude_files):
                continue

            name = unique_name(url_name, claimed)

            if name in existing:
                skipped += 1
                continue

            try:
                resp = requests.get(file_url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
            except requests.exceptions.Timeout:
                print(f"  Timed out: {file_url}")
                continue
            if resp.status_code != 200:
                print(f"  Skipping (HTTP {resp.status_code}): {file_url}")
                continue
            signature = _SIGNATURES.get(suffix)
            if signature and not resp.content.startswith(signature):
                print(f"  Skipping (not a {suffix} file): {file_url}")
                continue
            content = normalize_docx(resp.content) if suffix == ".docx" else resp.content
            digest = hashlib.sha256(content).digest()
            if digest in hashes:
                print(f"  Skipping (same as {hashes[digest]}): {file_url}")
                continue
            print(f"Downloading {file_url}")
            (out / name).write_bytes(content)
            existing.add(name)
            hashes[digest] = name

    if skipped:
        print(f"Skipped {skipped} already downloaded file(s)")
