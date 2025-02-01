from dataclasses import dataclass, field

from domain.document.value_object import (Conclusion, Introduction, ListSource,
                                          ListSupplement, TitlePage)
from src.domain.common.entity import BaseEntity


@dataclass(kw_only=True)
class Document(BaseEntity):
    title_page: TitlePage
    introduction: Introduction
    conclusion: Conclusion
    list_source: ListSource
    list_supplement: ListSupplement | None = field(default=None)