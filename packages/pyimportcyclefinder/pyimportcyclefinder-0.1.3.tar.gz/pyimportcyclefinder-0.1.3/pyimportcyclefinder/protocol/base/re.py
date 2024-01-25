import sys
from types import GenericAlias
from typing import (
    Any, AnyStr, Callable, Iterator, Optional, overload, Protocol, runtime_checkable, TypeVar
)

from typing_extensions import Literal, Self

try:
    from typing_extensions import Buffer
except ImportError:
    from typing_extensions.abc import Buffer

ReadableBuffer = Buffer
_T = TypeVar("_T")


@runtime_checkable
class ReBuiltInBasePatternProtocol(Protocol[AnyStr]):
    @overload
    def search(
            self: "ReBuiltInBasePatternProtocol[str]",
            string: str,
            pos: int = ...,
            endpos: int = ...,
            concurrent: bool | None = ...,
            timeout: float | None = ...,
    ) -> "Optional[ReBuiltInBaseMatchProtocol[str]]": ...

    @overload
    def search(
            self: "ReBuiltInBasePatternProtocol[bytes]",
            string: ReadableBuffer,
            pos: int = ...,
            endpos: int = ...,
            concurrent: bool | None = ...,
            timeout: float | None = ...,
    ) -> "Optional[ReBuiltInBaseMatchProtocol[bytes]]": ...

    @overload
    def match(
            self: "ReBuiltInBasePatternProtocol[str]",
            string: str,
            pos: int = ...,
            endpos: int = ...,
            concurrent: bool | None = ...,
            timeout: float | None = ...,
    ) -> "Optional[ReBuiltInBaseMatchProtocol[str]]": ...

    @overload
    def match(
            self: "ReBuiltInBasePatternProtocol[bytes]",
            string: ReadableBuffer,
            pos: int = ...,
            endpos: int = ...,
            concurrent: bool | None = ...,
            timeout: float | None = ...,
    ) -> "Optional[ReBuiltInBaseMatchProtocol[bytes]]": ...

    @overload
    def fullmatch(
            self: "ReBuiltInBasePatternProtocol[str]",
            string: str,
            pos: int = ...,
            endpos: int = ...,
            concurrent: bool | None = ...,
            timeout: float | None = ...,
    ) -> "Optional[ReBuiltInBaseMatchProtocol[str]]": ...

    @overload
    def fullmatch(
            self: "ReBuiltInBasePatternProtocol[bytes]",
            string: ReadableBuffer,
            pos: int = ...,
            endpos: int = ...,
            concurrent: bool | None = ...,
            timeout: float | None = ...,
    ) -> "Optional[ReBuiltInBaseMatchProtocol[bytes]]": ...

    @overload
    def split(
            self: "ReBuiltInBasePatternProtocol[str]", string: str, maxsplit: int = ...,
            concurrent: bool | None = ..., timeout: float | None = ...
    ) -> list[str | Any]: ...

    @overload
    def split(
            self: "ReBuiltInBasePatternProtocol[bytes]",
            string: ReadableBuffer,
            maxsplit: int = ...,
            concurrent: bool | None = ...,
            timeout: float | None = ...,
    ) -> list[bytes | Any]: ...

    @overload
    def findall(
            self: "ReBuiltInBasePatternProtocol[str]",
            string: str,
            pos: int = ...,
            endpos: int = ...,
            overlapped: bool = ...,
            concurrent: bool | None = ...,
            timeout: float | None = ...,
    ) -> list[Any]: ...

    @overload
    def findall(
            self: "ReBuiltInBasePatternProtocol[bytes]",
            string: ReadableBuffer,
            pos: int = ...,
            endpos: int = ...,
            overlapped: bool = ...,
            concurrent: bool | None = ...,
            timeout: float | None = ...,
    ) -> list[Any]: ...

    @overload
    def finditer(
            self: "ReBuiltInBasePatternProtocol[str]",
            string: str,
            pos: int = ...,
            endpos: int = ...,
            overlapped: bool = ...,
            concurrent: bool | None = ...,
            timeout: float | None = ...,
    ) -> "Iterator[ReBuiltInBaseMatchProtocol[str]]": ...

    @overload
    def finditer(
            self: "ReBuiltInBasePatternProtocol[bytes]",
            string: ReadableBuffer,
            pos: int = ...,
            endpos: int = ...,
            overlapped: bool = ...,
            concurrent: bool | None = ...,
            timeout: float | None = ...,
    ) -> "Iterator[ReBuiltInBaseMatchProtocol[bytes]]": ...

    @overload
    def sub(
            self: "ReBuiltInBasePatternProtocol[str]",
            repl: str | Callable[["ReBuiltInBaseMatchProtocol[str]"], str],
            string: str,
            count: int = ...,
            flags: int = ...,
            pos: int | None = ...,
            endpos: int | None = ...,
            concurrent: bool | None = ...,
            timeout: float | None = ...,
    ) -> str: ...

    @overload
    def sub(
            self: "ReBuiltInBasePatternProtocol[bytes]",
            repl: ReadableBuffer | Callable[["ReBuiltInBaseMatchProtocol[bytes]"], ReadableBuffer],
            string: ReadableBuffer,
            count: int = ...,
            flags: int = ...,
            pos: int | None = ...,
            endpos: int | None = ...,
            concurrent: bool | None = ...,
            timeout: float | None = ...,
    ) -> bytes: ...

    @overload
    def subn(
            self: "ReBuiltInBasePatternProtocol[str]",
            repl: str | Callable[["ReBuiltInBaseMatchProtocol[str]"], str],
            string: str,
            count: int = ...,
            flags: int = ...,
            pos: int | None = ...,
            endpos: int | None = ...,
            concurrent: bool | None = ...,
            timeout: float | None = ...,
    ) -> tuple[str, int]: ...

    @overload
    def subn(
            self: "ReBuiltInBasePatternProtocol[bytes]",
            repl: ReadableBuffer | Callable[["ReBuiltInBaseMatchProtocol[bytes]"], ReadableBuffer],
            string: ReadableBuffer,
            count: int = ...,
            flags: int = ...,
            pos: int | None = ...,
            endpos: int | None = ...,
            concurrent: bool | None = ...,
            timeout: float | None = ...,
    ) -> tuple[bytes, int]: ...


@runtime_checkable
class ReBuiltInBaseMatchProtocol(Protocol[AnyStr]):
    @overload
    def group(self, __group: Literal[0] = 0) -> AnyStr: ...

    @overload
    def group(self, __group: int | str = ...) -> AnyStr | Any: ...

    @overload
    def group(self, __group1: int | str, __group2: int | str, *groups: int | str) -> tuple[
        AnyStr | Any, ...]: ...

    @overload
    def groups(self, default: None = None) -> tuple[AnyStr | Any, ...]: ...

    @overload
    def groups(self, default: _T) -> tuple[AnyStr | _T, ...]: ...

    @overload
    def groupdict(self, default: None = None) -> dict[str, AnyStr | Any]: ...

    @overload
    def groupdict(self, default: _T) -> dict[str, AnyStr | _T]: ...

    @overload
    def span(self, __group: int | str = ...) -> tuple[int, int]: ...

    @overload
    def span(self, __group1: int | str, __group2: int | str, *groups: int | str) -> tuple[
        tuple[int, int], ...]: ...

    @overload
    def spans(self, __group: int | str = ...) -> list[tuple[int, int]]: ...

    @overload
    def spans(self, __group1: int | str, __group2: int | str, *groups: int | str) -> tuple[
        list[tuple[int, int]], ...]: ...

    @overload
    def start(self, __group: int | str = ...) -> int: ...

    @overload
    def start(self, __group1: int | str, __group2: int | str, *groups: int | str) -> tuple[
        int, ...]: ...

    @overload
    def starts(self, __group: int | str = ...) -> list[int]: ...

    @overload
    def starts(self, __group1: int | str, __group2: int | str, *groups: int | str) -> tuple[
        list[int], ...]: ...

    @overload
    def end(self, __group: int | str = ...) -> int: ...

    @overload
    def end(self, __group1: int | str, __group2: int | str, *groups: int | str) -> tuple[
        int, ...]: ...

    @overload
    def ends(self, __group: int | str = ...) -> list[int]: ...

    @overload
    def ends(self, __group1: int | str, __group2: int | str, *groups: int | str) -> tuple[
        list[int], ...]: ...

    def expand(self, template: AnyStr) -> AnyStr: ...

    def expandf(self, format: AnyStr) -> AnyStr: ...

    @overload
    def captures(self, __group: int | str = ...) -> list[AnyStr]: ...

    @overload
    def captures(self, __group1: int | str, __group2: int | str, *groups: int | str) -> tuple[
        list[AnyStr], ...]: ...

    def capturesdict(self) -> dict[str, list[AnyStr]]: ...

    def detach_string(self) -> None: ...

    def allcaptures(self) -> tuple[list[AnyStr]]: ...

    def allspans(self) -> tuple[list[tuple[int, int]]]: ...

    @overload
    def __getitem__(self, __key: Literal[0]) -> AnyStr: ...

    @overload
    def __getitem__(self, __key: int | str) -> AnyStr | Any: ...

    def __copy__(self) -> Self: ...

    def __deepcopy__(self) -> Self: ...

    if sys.version_info >= (3, 9):
        def __class_getitem__(cls, item: Any) -> GenericAlias: ...


@runtime_checkable
class ReBuiltInBaseScannerProtocol(Protocol[AnyStr]):
    def __iter__(self) -> Self: ...

    def __next__(self) -> ReBuiltInBaseMatchProtocol[AnyStr]: ...

    def match(self) -> Optional[ReBuiltInBaseMatchProtocol[AnyStr]]: ...

    def search(self) -> Optional[ReBuiltInBaseMatchProtocol[AnyStr]]: ...
