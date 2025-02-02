from dataclasses import dataclass, field

from src.domain.common.entity import BaseEntity
from src.domain.document.value_object import Section, TitlePage


@dataclass(kw_only=True)
class Document(BaseEntity):
    user_uuid: str
    name: str
    title_page: TitlePage
    introduction: str
    main_sections: list[Section]
    conclusion: str
    references: list[str]
    appendices: list[str] | None = field(default=None)
