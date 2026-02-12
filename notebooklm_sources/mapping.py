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
    },
    "inf2-iads": {
        "sources": {
            "url": "https://opencourse.inf.ed.ac.uk/inf2-iads/course-materials/semester-1/schedule"
            # sem 2 https://opencourse.inf.ed.ac.uk/inf2-iads/course-materials/semester-2/schedule
        }
    },
    # "inf2-sepp": {
    #     "sources": {
    #         "url": "https://opencourse.inf.ed.ac.uk/inf2-sepp/schedule"
    #     }
    # },
    "inf2-fds": {
        "sources": {
            "url": "https://opencourse.inf.ed.ac.uk/inf2-fds/course-materials/",
            "week": "semester-*",
            "lecture": "week-*"
        }
    }
}