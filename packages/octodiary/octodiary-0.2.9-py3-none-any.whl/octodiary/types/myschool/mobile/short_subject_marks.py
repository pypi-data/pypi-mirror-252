#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

import datetime
from typing import Any, Optional

from octodiary.types.model import Type


class Path(Type):
    value: Optional[int] = None
    remain: Optional[int] = None
    weight: Optional[int] = None


class TargetItem(Type):
    value: Optional[int] = None
    remain: Optional[int] = None
    round: Optional[str] = None
    paths: Optional[list[Path]] = []


class Grade(Type):
    origin: Optional[str] = None
    five: Optional[int] = None
    hundred: Optional[int] = None


class Value(Type):
    name: Optional[Any] = None
    grade: Optional[Grade] = None
    grade_system_id: Optional[Any] = None
    grade_system_type: Optional[str] = None


class Criterion(Type):
    name: Optional[Any] = None
    value: Optional[str] = None


class Mark(Type):
    id: Optional[int] = None
    value: Optional[str] = None
    values: Optional[list[Value]] = []
    comment: Optional[str] = None
    weight: Optional[int] = None
    point_date: Optional[datetime.datetime | datetime.date] = None
    control_form_name: Optional[str] = None
    comment_exists: Optional[bool] = None
    created_at: Optional[datetime.datetime | datetime.date] = None
    updated_at: Optional[datetime.datetime | datetime.date] = None
    criteria: Optional[list[Criterion]] = []
    date: Optional[str] = None
    is_exam: Optional[bool] = None
    is_point: Optional[bool] = None
    original_grade_system_type: Optional[str] = None


class PayloadItem(Type):
    average: Optional[str]
    dynamic: Optional[str] = None
    period: Optional[str]
    count: Optional[int]
    target: Optional[TargetItem]
    marks: Optional[list[Mark]]
    start: Optional[str]
    end: Optional[str]
    subject_name: Optional[str] = None
    subject_id: Optional[int] = None
    fixed_value: Optional[str] = None


class ShortSubjectMarks(Type):
    payload: Optional[list[PayloadItem]] = None
