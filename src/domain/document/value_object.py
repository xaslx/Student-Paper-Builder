from src.domain.common.value_object import BaseValueObject
from dataclasses import dataclass, field

from dataclasses import dataclass, field
from datetime import datetime



@dataclass(kw_only=True)
class TitlePage(BaseValueObject):
    
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


@dataclass
class Introduction(BaseValueObject):
    
    text: str


@dataclass
class Conclusion(BaseValueObject):
    
    text: str


@dataclass
class ListSource(BaseValueObject):
    list_text: list[str]
    

@dataclass
class ListSupplement(BaseValueObject):
    list_text: list[str]