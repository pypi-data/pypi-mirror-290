import re
from enum import Enum
from re import Pattern
from typing import (
    ClassVar,
    Literal,
)

from bs4 import NavigableString, PageElement, Tag
from get_build_info import get_building_map, get_building_map_rev
from get_dpt_map import get_dpt_code_map, get_dpt_name_map, get_full_name_map
from pydantic.dataclasses import dataclass

type Label = Literal[
    "serial",
    "department",
    "code",
    "class_id",
    "title",
    "field_expertise",
    "credits",
    "id",
    "duration",
    "category",
    "instructor",
    "enrollment_rule",
    "schedule",
    "max_students",
    "restrictions",
    "remarks",
    "website",
]


RAW_LABEL_MAP: dict[Label, str] = {
    "serial": "流水號",
    "department": "授課對象",
    "code": "課號",
    "class_id": "班次",
    "title": "課程名稱",
    "field_expertise": "領域專長",
    "credits": "學分",
    "id": "課程識別碼",
    "duration": "全/半年",
    "category": "必/選修",
    "instructor": "授課教師",
    "enrollment_rule": "加選方式",
    "schedule": "時間教室",
    "max_students": "總人數",
    "restrictions": "選課限制條件",
    "remarks": "備註",
    "website": "課程網頁",
}

LABEL_MAP: dict[str, Label] = {v: k for k, v in RAW_LABEL_MAP.items()}


def get_raw_label(label: Label) -> str:
    return RAW_LABEL_MAP[label]


@dataclass
class Department:
    name: str
    code: str


class Duration(Enum):
    FULL = "全年"
    HALF = "半年"


class Category(Enum):
    REQUIRED = "必修"
    AUTO_ENROLLED = "必帶"
    ELECTIVE = "選修"


class EnrollmentRule(Enum):
    OPEN = 1
    APPROVAL = 2
    ALLOCATION = 3


@dataclass
class Classroom:
    uid: str
    name: str

    uid_pattern: ClassVar[Pattern[str]] = re.compile(r"uid=(.+)")

    @classmethod
    def from_tag(cls, tag: PageElement | None):
        if not tag or not isinstance(tag, Tag) or tag.name != "a":
            raise ValueError("Tag is not an anchor element")

        name = tag.text[1:-1]
        if not isinstance((href := tag["href"]), str):
            raise ValueError(f"Unexpected href: ${repr(href)}")
        if res := cls.uid_pattern.search(href):
            uid = res.group(1)
        else:
            uid = get_building_map_rev()[name]
        return Classroom(uid, name)


@dataclass
class ClassPeriod:
    day: int  # 0-6
    start: int
    end: int
    classroom: Classroom

    DAY_MAP: ClassVar = {
        "日": 0,  # ? unused
        "一": 1,
        "二": 2,
        "三": 3,
        "四": 4,
        "五": 5,
        "六": 6,
    }

    @classmethod
    def get_day(cls, raw_day: str) -> int:
        return cls.DAY_MAP[raw_day]


@dataclass
class Schedule:
    periods: list[ClassPeriod]

    pattern: ClassVar[Pattern[str]] = re.compile(r"([^\s]+?)\((.+?)\)")

    @classmethod
    def from_str(cls, text: str):
        periods: list[ClassPeriod] = []
        for match in cls.pattern.finditer(text):
            raw_day = match.group(1)[0]
            raw_periods = match.group(1)[1:]
            raw_classroom = match.group(2)
            for raw_period in raw_periods.split(","):
                # periods.append(
                #     ClassPeriod.from_partial_raw(raw_day, raw_period, raw_classroom)
                # )
                raise NotImplementedError

        return Schedule(periods)

    @classmethod
    def from_tag(cls, tag: Tag):
        periods: list[ClassPeriod] = []

        s: NavigableString
        for s in tag.find_all(string=True, recursive=False):
            day = ClassPeriod.get_day(s[0])
            sub_periods = list(map(int, s[1:].split(",")))
            st, end = sub_periods[0], sub_periods[-1]
            assert list(range(st, end + 1)) == sub_periods
            class_room = Classroom.from_tag(s.next_element)
            periods.append(ClassPeriod(day, st, end, class_room))
        return Schedule(periods)


def parse_tag(tag: Tag, label: Label):
    text = tag.text.strip()
    match label:
        case "serial":
            return int(text)
        case "department":
            try:
                dpt_code_map = get_dpt_code_map()
                dpt_full_name_map = get_full_name_map()
                return Department(name=text, code=dpt_code_map[dpt_full_name_map[text]])
            except KeyError:
                return Department(name=text, code="")
        case "code":
            return text
        case "class_id":
            return text
        case "title":
            return text
        case "field_expertise":
            return text
        case "credits":
            return float(text)
        case "id":
            return text
        case "duration":
            return Duration(text)
        case "category":
            return Category(text)
        case "instructor":
            return text
        case "enrollment_rule":
            return EnrollmentRule(int(text))
        case "schedule":
            return Schedule.from_tag(tag)
        case "max_students":
            return int(re.sub(r"\(.*?\)", "", text))
        case "restrictions":
            return text
        case "remarks":
            return text
        case "website":
            return text

    raise TypeError(f"Unknown label: {label}")
