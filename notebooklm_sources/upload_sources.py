from pathlib import Path
from urllib.parse import urlparse

from notebooklm_tools.core.auth import get_auth_manager
from notebooklm_tools.core.client import NotebookLMClient


def notebook_id_from_ref(notebook_ref: str) -> str:
    parsed = urlparse(notebook_ref)
    if not parsed.scheme:
        return notebook_ref

    path_parts = [part for part in parsed.path.split("/") if part]
    try:
        notebook_index = path_parts.index("notebook")
    except ValueError as exc:
        raise ValueError(f"Notebook URL does not contain a notebook id: {notebook_ref}") from exc

    try:
        return path_parts[notebook_index + 1]
    except IndexError as exc:
        raise ValueError(f"Notebook URL does not contain a notebook id: {notebook_ref}") from exc


def get_client(profile: str | None = None) -> NotebookLMClient:
    manager = get_auth_manager(profile)
    if not manager.profile_exists():
        profile_name = manager.profile_name
        raise RuntimeError(
            f"NotebookLM auth profile '{profile_name}' was not found. "
            "Run `uv run nlm login` before uploading sources."
        )

    auth_profile = manager.load_profile()
    return NotebookLMClient(
        cookies=auth_profile.cookies,
        csrf_token=auth_profile.csrf_token or "",
        session_id=auth_profile.session_id or "",
        build_label=auth_profile.build_label or "",
    )


def list_uploaded(client: NotebookLMClient, notebook_id: str) -> set[str]:
    sources = client.get_notebook_sources_with_types(notebook_id)

    return {
        source["title"]
        for source in sources
        if isinstance(source.get("title"), str)
    }


def upload_sources(
    notebook_ref: str,
    files: list[Path | str],
    *,
    profile: str | None = None,
    wait: bool = True,
    wait_timeout: float = 600.0,
) -> None:
    if not files:
        return

    notebook_id = notebook_id_from_ref(notebook_ref)
    files = [Path(file) for file in files]

    with get_client(profile) as client:
        already_uploaded = list_uploaded(client, notebook_id)

        new_files = [file for file in files if file.name not in already_uploaded]

        skipped = len(files) - len(new_files)
        if skipped:
            print(f"Skipping {skipped} already uploaded file(s)")

        for file in new_files:
            print(f"Uploading {file.name}")
            client.add_file(
                notebook_id,
                file,
                wait=wait,
                wait_timeout=wait_timeout,
            )

    if new_files:
        print(f"Uploaded {len(new_files)} file(s)")
