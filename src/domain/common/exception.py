from dataclasses import dataclass
from typing import ClassVar


@dataclass(eq=False)
class AppError(Exception):

    @property
    def message(self) -> str:
        return 'An app error occurred'


@dataclass(eq=False)
class DomainError(AppError):

    @property
    def message(self) -> str:
        return 'A domain error occurred'