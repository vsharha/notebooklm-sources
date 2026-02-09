from typing import TypedDict, Required


class SourcesConfig(TypedDict, total=False):
    url: Required[str]
    week: str
    lecture: str


class CourseConfig(TypedDict):
    sources: SourcesConfig
    notebook_url: str


mapping: dict[str, CourseConfig] = {
    "inf2d": {
        "sources": {
            "url": "https://opencourse.inf.ed.ac.uk/inf2d",
            "week": "week-*",
            "lecture": "lecture-*",
        },
        "notebook_url": "https://notebooklm.google.com/notebook/5e8b1c41-babf-456c-a47c-b5f3b85528ef",
    }
}