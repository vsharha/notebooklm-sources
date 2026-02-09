from pathlib import Path
from patchright.sync_api import sync_playwright

def upload_files(files: list[Path | str], page, notebook_url: str):
    files: list[Path] = [Path(file) for file in files]

    page.goto(f"{notebook_url}?addSource=true")

    page.wait_for_selector(".drop-zone")

    with page.expect_file_chooser() as fc_info:
        page.locator(".drop-zone").get_by_text("Upload files").click()

    file_chooser = fc_info.value
    file_chooser.set_files(files)

    page.wait_for_selector(
        ".single-source-container .select-checkbox-container .loading-spinner",
    )
    page.wait_for_selector(
        ".single-source-container .select-checkbox-container .loading-spinner",
        state="hidden",
        timeout=0,
    )

def wait_for_stable_count(page, selector, interval=1000):
    locator = page.locator(selector)
    prev_count = None
    while True:
        page.wait_for_timeout(interval)
        count = locator.count()
        if count == prev_count:
            return
        prev_count = count

def list_uploaded(page) -> set[str]:
    wait_for_stable_count(page, ".single-source-container .source-title-column span")

    return set([
        label.text_content()
        for label in page.locator(".single-source-container .source-title-column span").all()
    ])

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

        already_uploaded = list_uploaded(page)

        new_files = [
            f for f in files
            if Path(f).name not in already_uploaded
        ]

        skipped = len(files) - len(new_files)
        if skipped:
            print(f"Skipping {skipped} already uploaded file(s)")

        if not new_files:
            context.close()
            return

        upload_files(new_files, page, notebook_url)

        print(f"Uploaded {len(new_files)} file(s)")

        context.close()