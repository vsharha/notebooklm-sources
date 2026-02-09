from notebooklm_sources.pdf_page import collect_links
from notebooklm_sources.pdf import download_pdfs_from_pages

def main():
    start_url = input("Enter course page URL > ").strip()

    week_path = input(
        "Enter week path pattern (empty = use start page only) > "
    ).strip()

    lecture_path = input(
        "Enter lecture path pattern (empty = use week pages directly) > "
    ).strip()

    # Original behavior
    if not week_path:
        pages = {start_url}

    # Week pages only
    elif week_path and not lecture_path:
        pages = collect_links(start_url, week_path)

    # Week → lecture
    else:
        weeks = collect_links(start_url, week_path)
        pages = set()
        for week in weeks:
            pages |= collect_links(week, lecture_path)

    subdir = input("Enter subdirectory name (empty = none) > ").strip()

    print(f"Using {len(pages)} page(s)")
    download_pdfs_from_pages(pages, subdir=subdir)

if __name__ == "__main__":
    main()