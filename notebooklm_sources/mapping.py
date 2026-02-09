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
        "notebook_url": "https://notebooklm.google.com/notebook/4021c72f-68df-41da-bd67-193538009614",
    }
}