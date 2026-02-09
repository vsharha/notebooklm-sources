from pathlib import Path
from patchright.sync_api import sync_playwright

def upload_files(files: list[Path | str], page):
    files: list[Path] = [Path(file) for file in files]

    page.locator(".add-source-button").click()

    with page.expect_file_chooser() as fc_info:
        page.locator(".drop-zone").get_by_text("Upload files").click()

    file_chooser = fc_info.value
    file_chooser.set_files(files)

def upload_sources(notebook_url: str, files: list[Path | str]):
    with sync_playwright() as playwright:
        context = playwright.chromium.launch_persistent_context(
            user_data_dir="profile",
            headless=False
        )

        if context.pages:
            page = context.pages[0]
        else:
            page = context.new_page()

        page.goto(notebook_url)
        if page.url != notebook_url:
            print("Waiting for authentication...")
            page.wait_for_url(notebook_url, timeout = 2 * 60 * 1000)

        for file in files:
            upload_file(file, page)