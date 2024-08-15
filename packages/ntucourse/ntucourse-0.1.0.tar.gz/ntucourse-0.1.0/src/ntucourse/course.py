from typing import Any

from label import (
    RAW_LABEL_MAP,
    Category,
    Department,
    Duration,
    EnrollmentRule,
    Schedule,
)
from pydantic.dataclasses import dataclass
from search import Row


@dataclass
class Course:
    serial: int
    department: Department
    code: str
    class_id: str
    title: str
    field_expertise: str
    credits: float
    id: str
    duration: Duration
    category: Category
    instructor: str
    enrollment_rule: EnrollmentRule
    schedule: Schedule
    max_students: int
    restrictions: str
    remarks: str
    website: str

    @staticmethod
    def from_row(row: Row):
        labels = RAW_LABEL_MAP.keys()
        kwargs: dict[str, Any] = {label: row[label] for label in labels}

        return Course(**kwargs)
