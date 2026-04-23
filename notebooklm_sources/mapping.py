from typing import NotRequired, Required, TypedDict


class SourcesConfig(TypedDict, total=False):
    url: Required[str]
    patterns: list[str]


class CourseConfig(TypedDict):
    sources: SourcesConfig
    notebook_url: NotRequired[str]


mapping: dict[str, CourseConfig] = {
    "inf2d": {
        "sources": {
            "url": "https://opencourse.inf.ed.ac.uk/inf2d/course-materials",
            "patterns": ["week-*", "lecture-*"],
        },
        "notebook_url": "https://notebooklm.google.com/notebook/7733edc5-7ed2-4e59-b0be-a53dce198a26",
    },
    "inf2-iads": {
        "sources": {
            "url": "https://opencourse.inf.ed.ac.uk/inf2-iads/course-materials",
            "patterns": ["semester-{n}", "schedule"],
        },
        "notebook_url": "https://notebooklm.google.com/notebook/0fc9e3d6-de9e-47dc-980c-055f35b70ac2",
    },
    "inf2-fds": {
        "sources": {
            "url": "https://opencourse.inf.ed.ac.uk/inf2-fds/resource-list",
        },
        "notebook_url": "https://notebooklm.google.com/notebook/fcf1a72f-3ccf-457d-9996-7f819791c413"
    },
    "inf2-sepp": {
        "sources": {
            "url": "https://opencourse.inf.ed.ac.uk/inf2-sepp/schedule"
        }   
    },
}
