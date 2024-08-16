from collections.abc import Mapping
from typing import TypedDict


class X(TypedDict):
    a: int


def f(d: type[Mapping]) -> None:
    pass


f(X)
