from enum import Enum
from typing import Any, List

from .dataclasses import dataclass


def sort_errors_by_field(error):
    return error.field


class Status(Enum):
    ok = 0
    not_found = 1
    not_ready = 2
    invalid = 3
    duplicated = 4
    unauthenticated = 5
    forbidden = 6
    conflict = 7
    server_error = 8
    unprocessable_entry = 9


class ErrorTypes(Enum):
    invalid = 0
    duplicated = 1
    required = 2
    not_found = 3
    rule = 4


@dataclass
class FieldError:
    field: str
    type: ErrorTypes
    msg: str = ""
    params: object = None


@dataclass
class Resp:
    status: Status = Status.ok
    errors: List[FieldError] = None

    @property
    def ok(self):
        return self.status == Status.ok

    def __post_init__(self):
        if self.errors:
            self.errors.sort(key=sort_errors_by_field)


@dataclass
class ItemResp(Resp):
    item: Any = None


@dataclass
class ItemsResp(Resp):
    items: List[Any] = None


@dataclass
class PageResp(Resp):
    items: List[Any] = None
    cursor: int = None
    next_cursor: int = None
    previous_cursor: int = None

