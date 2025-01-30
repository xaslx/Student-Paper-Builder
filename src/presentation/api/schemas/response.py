from dataclasses import dataclass, field
from typing import Generic, TypeVar, Any
from pydantic import BaseModel, Field


TResult = TypeVar('TResult')
TError = TypeVar('TError')
TData = TypeVar('TData')


@dataclass(frozen=True)
class Response:
    ...


@dataclass(frozen=True)
class ErrorData(Generic[TError]):
    title: str = 'Unknown error occurred'
    data: TError | None = None


@dataclass(frozen=True)
class ErrorResponse(Response, Generic[TError]):
    status: int = 500
    error: ErrorData[TError] = field(default_factory=ErrorData)
    
    
class ApiResponse(BaseModel, Generic[TData]):
    data: TData | dict = Field(default_factory=dict)
    meta: dict[str, Any] = Field(default_factory=dict)
