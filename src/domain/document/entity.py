from dataclasses import dataclass, field, fields, replace, asdict

from src.presentation.schemas.document import UpdateDocument
from src.domain.common.entity import BaseEntity
from src.domain.document.value_object import Application, Section, TitlePage


@dataclass(kw_only=True)
class Document(BaseEntity):
    user_uuid: str
    name: str
    title_page: TitlePage
    abbreviations: list[str]
    introduction: str
    main_sections: list[Section]
    conclusion: str
    references: list[str]
    appendices: list[Application] | None = field(default=None)


    def update(self, new_data: UpdateDocument):
        
        updated_title_page = replace(self.title_page, **{
            k: v for k, v in new_data.title_page.model_dump().items() if v is not None
        }) if new_data.title_page else self.title_page

        self.name = new_data.name or self.name
        self.introduction = new_data.introduction or self.introduction
        self.conclusion = new_data.conclusion or self.conclusion
        self.title_page = updated_title_page or self.title_page
        self.updated_at = new_data.updated_at or self.updated_at
        
        if new_data.abbreviations is not None:
            self.abbreviations = new_data.abbreviations
            
        if new_data.references is not None:
            self.references = new_data.references

        if new_data.main_sections is not None:
            self.main_sections = new_data.main_sections
        
        if new_data.appendices is not None:
            self.appendices = new_data.appendices