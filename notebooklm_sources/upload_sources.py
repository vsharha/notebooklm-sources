from pathlib import Path
from patchright.sync_api import sync_playwright

def upload_files(files: list[Path | str], page):
    files: list[Path] = [Path(file) for file in files]

    page.wait_for_selector(".add-source-button")

    page.locator(".add-source-button").click()

    page.wait_for_selector(".drop-zone")

    with page.expect_file_chooser() as fc_info:
        page.locator(".drop-zone").get_by_text("Upload files").click()

    file_chooser = fc_info.value
    file_chooser.set_files(files)

def list_uploaded(page) -> list[str]:
    page.wait_for_load_state("domcontentloaded")

    return [
        source.locator(".source-title-column").text_content()
        for source in page.locator(".single-source-container").all()
    ]

def upload_sources(notebook_url: str, files: list[Path | str]):
    if not files:
        return

    with sync_playwright() as playwright:
        context = playwright.chromium.launch_persistent_context(
            user_data_dir="profile",
            headless=False,
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = context.pages[0] if context.pages else context.new_page()

        page.goto(notebook_url)
        if not page.url.startswith(notebook_url):
            print("Waiting for authentication...")
            page.wait_for_url(f"{notebook_url}**", timeout=2 * 60 * 1000)

        already_uploaded = set(list_uploaded(page))
        new_files = [
            f for f in files
            if Path(f).stem not in already_uploaded
        ]

        skipped = len(files) - len(new_files)
        if skipped:
            print(f"Skipping {skipped} already uploaded file(s)")

        if not new_files:
            context.close()
            return

        upload_files(new_files, page)
        context.close()