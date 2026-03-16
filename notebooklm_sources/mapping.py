from typing import TypedDict, Required


class SourcesConfig(TypedDict, total=False):
    url: Required[str]
    patterns: list[str]


class CourseConfig(TypedDict):
    sources: SourcesConfig
    notebook_url: str


mapping: dict[str, CourseConfig] = {
    # "inf2d": {
    #     "sources": {
    #         "url": "https://opencourse.inf.ed.ac.uk/inf2d/course-materials",
    #         "patterns": ["week-*", "lecture-*"],
    #     },
    #     "notebook_url": "https://notebooklm.google.com/notebook/5e8b1c41-babf-456c-a47c-b5f3b85528ef",
    # },
    "inf2-iads": {
        "sources": {
            "url": "https://opencourse.inf.ed.ac.uk/inf2-iads/course-materials",
            "patterns": ["semester-{n}", "schedule"],
        },
        "notebook_url": "https://notebooklm.google.com/notebook/ea1aa2a7-401e-4695-a5d1-4011f4d4bda8",
    },
    # "inf2-sepp": {
    #     "sources": {
    #         "url": "https://opencourse.inf.ed.ac.uk/inf2-sepp/schedule"
    #     }
    # },
    # "inf2-fds": {
    #     "sources": {
    #         "url": "https://opencourse.inf.ed.ac.uk/inf2-fds/course-materials/",
    #         "patterns": ["semester-*", "week-*"],
    #     }
    # }
}