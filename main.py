from pathlib import Path

from notebooklm_sources.mapping import mapping, SourcesConfig
from notebooklm_sources.pdf_page import collect_links, collect_indexed_pages
from notebooklm_sources.pdf import download_pdfs_from_pages
from notebooklm_sources.upload_sources import upload_sources


def resolve_pages(sources: SourcesConfig) -> set[str]:
    pages = {sources["url"]}
    for pattern in sources.get("patterns", []):
        next_pages = set()
        for page in pages:
            if "{n}" in pattern:
                next_pages |= collect_indexed_pages(page, pattern)
            else:
                next_pages |= collect_links(page, pattern)
        pages = next_pages
    return pages


def process_course(course_name: str, config):
    print(f"\n{'=' * 40}")
    print(f"Processing: {course_name}")
    print(f"{'=' * 40}")

    pages = resolve_pages(config["sources"])
    print(f"Found {len(pages)} page(s)")

    download_pdfs_from_pages(pages, subdir=course_name)
    notebook_url = config.get("notebook_url")
    if not notebook_url:
        print("No notebook URL configured; nothing was uploaded.")
        return

    image_dir = Path("pdfs") / course_name / "image"
    if not image_dir.exists():
        print(f"No image PDFs found in {image_dir}")
        return

    image_pdfs = sorted(p for p in image_dir.iterdir() if p.suffix.lower() == ".pdf")
    if not image_pdfs:
        print(f"No image PDFs found in {image_dir}")
        return

    print(f"Found {len(image_pdfs)} image PDF(s) to upload")
    upload_sources(notebook_url, image_pdfs)


def main():
    for course_name, config in mapping.items():
        process_course(course_name, config)


if __name__ == "__main__":
    main()
