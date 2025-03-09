from src.domain.common.value_object import BaseValueObject
from dataclasses import dataclass, field

from dataclasses import dataclass, field
from datetime import datetime



@dataclass(kw_only=True, frozen=True)
class TitlePage:
    
    type_of_work: str
    discipline: str
    subject: str
    educational_institution: str
    year: int = field(default_factory=lambda: datetime.now().year)
    student_fullname: str
    teacher_fullname: str
    faculty: str
    city: str
    teaching_position: str
    created_at: datetime = field(default_factory=lambda: datetime.now())
    updated_at: datetime | None = field(default=None)


@dataclass(frozen=True, kw_only=True)
class Section:
    title: str
    content: str
    subsection: str | None


@dataclass(frozen=True, kw_only=True)
class Application:
    path: str
    description: str
    name: str