import json
import os
import pathlib
from typing import Literal

from course import Course
from label import ClassPeriod, Schedule
from pydantic import RootModel
from search import QueryType, Search

course_codes = [
    "Med2022",
    "Med3070",
    "IMP5004",
    "HPM5022",
    "CSIE2121",
]
course_semesters = [
    "113-1",
    "113-1",
    "113-1",
    "112-2",
    "112-2",
]

courses: list[Course] = []
for code, semester in zip(course_codes, course_semesters):
    search = Search(
        QueryType.CODE,
        code,
        semester,
    )
    courses.append(Course.from_row(search.rows[0]))

Courses = RootModel[list[Course]]
fp = open(pathlib.Path(__file__).parent / "../../courses_schema.json", "w+")
json.dump(Courses.model_json_schema(), fp, indent=4, ensure_ascii=False)

open(pathlib.Path(__file__).parent / "../../src/assets/courses.json", "w+").write(
    Courses(courses).model_dump_json(indent=4)
)

# TODO: to dict
# TODO: index

# print(search.rows[0])
