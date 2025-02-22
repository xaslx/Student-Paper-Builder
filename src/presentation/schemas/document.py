from pydantic import BaseModel, Field
from datetime import datetime


class TitlePage(BaseModel):
    type_of_work: str | None = Field(default=None)
    discipline: str | None = Field(default=None)
    subject: str | None = Field(default=None)
    educational_institution: str | None = Field(default=None)
    year: int | None = Field(default=None)
    student_fullname: str | None = Field(default=None)
    teacher_fullname: str | None = Field(default=None)
    faculty: str | None = Field(default=None)
    city: str | None = Field(default=None)
    teaching_position: str | None = Field(default=None)


class Section(BaseModel):
    title: str | None = Field(default=None)
    content: str | None = Field(default=None)
    subsection: str | None = Field(default=None)


class CreateDocument(BaseModel):
    title_page: TitlePage
    name: str = Field(min_length=5, max_length=50, default=None)
    introduction: str | None = Field(default=None)
    abbreviations: list[str] | None = Field(default=None)
    main_sections: list[Section] | None = Field(default=None)
    conclusion: str | None = Field(default=None)
    references: list[str] | None = Field(default=None)
    appendices: list[str] | None = Field(default=None)
    

class UpdateDocument(CreateDocument):
    title_page: TitlePage | None = Field(default=None)
    updated_at: datetime = Field(default_factory=datetime.now)