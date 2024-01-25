import sys
from types import GenericAlias
from typing import (
    Any, AnyStr, Callable, Optional, overload, Protocol, runtime_checkable, TypeVar, Union
)

from typing_extensions import Literal, Self

try:
    from typing_extensions import Buffer
except ImportError:
    from typing_extensions.abc import Buffer

ReadableBuffer = Buffer
_T = TypeVar("_T")


@runtime_checkable
class BaseRegexPackagePatternProtocol(Protocol[AnyStr]):
    @overload
    def search(
            self: "BaseRegexPackagePatternProtocol[str]",
            string: str,
            pos: int = ...,
            endpos: int = ...,
            concurrent: bool | None = ...,
            timeout: float | None = ...,
    ) -> "Optional[BaseRegexPackageMatchProtocol[str]]": ...

    @overload
    def search(
            self: "BaseRegexPackagePatternProtocol[bytes]",
            string: ReadableBuffer,
            pos: int = ...,
            endpos: int = ...,
            concurrent: bool | None = ...,
            timeout: float | None = ...,
    ) -> "Optional[BaseRegexPackageMatchProtocol[bytes]]": ...

    @overload
    def match(
            self: "BaseRegexPackagePatternProtocol[str]",
            string: str,
            pos: int = ...,
            endpos: int = ...,
            concurrent: bool | None = ...,
            timeout: float | None = ...,
    ) -> "Optional[BaseRegexPackageMatchProtocol[str]]": ...

    @overload
    def match(
            self: "BaseRegexPackagePatternProtocol[bytes]",
            string: ReadableBuffer,
            pos: int = ...,
            endpos: int = ...,
            concurrent: bool | None = ...,
            timeout: float | None = ...,
    ) -> "Optional[BaseRegexPackageMatchProtocol[bytes]]": ...

    @overload
    def fullmatch(
            self: "BaseRegexPackagePatternProtocol[str]",
            string: str,
            pos: int = ...,
            endpos: int = ...,
            concurrent: bool | None = ...,
            timeout: float | None = ...,
    ) -> "Optional[BaseRegexPackageMatchProtocol[str]]": ...

    @overload
    def fullmatch(
            self: "BaseRegexPackagePatternProtocol[bytes]",
            string: ReadableBuffer,
            pos: int = ...,
            endpos: int = ...,
            concurrent: bool | None = ...,
            timeout: float | None = ...,
    ) -> "Optional[BaseRegexPackageMatchProtocol[bytes]]": ...

    @overload
    def split(
            self: "BaseRegexPackagePatternProtocol[str]", string: str, maxsplit: int = ...,
            concurrent: bool | None = ..., timeout: float | None = ...
    ) -> list[str | Any]: ...

    @overload
    def split(
            self: "BaseRegexPackagePatternProtocol[bytes]",
            string: ReadableBuffer,
            maxsplit: int = ...,
            concurrent: bool | None = ...,
            timeout: float | None = ...,
    ) -> list[bytes | Any]: ...

    @overload
    def splititer(
            self: "BaseRegexPackagePatternProtocol[str]", string: str, maxsplit: int = ...,
            concurrent: bool | None = ..., timeout: float | None = ...
    ) -> "BaseSplitterProtocol[str]": ...

    @overload
    def splititer(
            self: "BaseRegexPackagePatternProtocol[bytes]",
            string: ReadableBuffer,
            maxsplit: int = ...,
            concurrent: bool | None = ...,
            timeout: float | None = ...,
    ) -> "BaseSplitterProtocol[bytes]": ...

    @overload
    def findall(
            self: "BaseRegexPackagePatternProtocol[str]",
            string: str,
            pos: int = ...,
            endpos: int = ...,
            overlapped: bool = ...,
            concurrent: bool | None = ...,
            timeout: float | None = ...,
    ) -> list[Any]: ...

    @overload
    def findall(
            self: "BaseRegexPackagePatternProtocol[bytes]",
            string: ReadableBuffer,
            pos: int = ...,
            endpos: int = ...,
            overlapped: bool = ...,
            concurrent: bool | None = ...,
            timeout: float | None = ...,
    ) -> list[Any]: ...

    @overload
    def finditer(
            self: "BaseRegexPackagePatternProtocol[str]",
            string: str,
            pos: int = ...,
            endpos: int = ...,
            overlapped: bool = ...,
            concurrent: bool | None = ...,
            timeout: float | None = ...,
    ) -> "BaseRegexPackageScannerProtocol[str]": ...

    @overload
    def finditer(
            self: "BaseRegexPackagePatternProtocol[bytes]",
            string: ReadableBuffer,
            pos: int = ...,
            endpos: int = ...,
            overlapped: bool = ...,
            concurrent: bool | None = ...,
            timeout: float | None = ...,
    ) -> "BaseRegexPackageScannerProtocol[bytes]": ...

    @overload
    def sub(
            self: "BaseRegexPackagePatternProtocol[str]",
            repl: str | Callable[["BaseRegexPackageMatchProtocol[str]"], str],
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
            self: "BaseRegexPackagePatternProtocol[bytes]",
            repl: Union[
                  ReadableBuffer,
                  Callable[["BaseRegexPackageMatchProtocol[bytes]"], ReadableBuffer]
            ],
            string: ReadableBuffer,
            count: int = ...,
            flags: int = ...,
            pos: int | None = ...,
            endpos: int | None = ...,
            concurrent: bool | None = ...,
            timeout: float | None = ...,
    ) -> bytes: ...

    @overload
    def subf(
            self: "BaseRegexPackagePatternProtocol[str]",
            format: str | Callable[["BaseRegexPackageMatchProtocol[str]"], str],
            string: str,
            count: int = ...,
            flags: int = ...,
            pos: int | None = ...,
            endpos: int | None = ...,
            concurrent: bool | None = ...,
            timeout: float | None = ...,
    ) -> str: ...

    @overload
    def subf(
            self: "BaseRegexPackagePatternProtocol[bytes]",
            format: Union[
                ReadableBuffer,
                Callable[
                    ["BaseRegexPackageMatchProtocol[bytes]"],
                    ReadableBuffer
                ]
            ],
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
            self: "BaseRegexPackagePatternProtocol[str]",
            repl: str | Callable[["BaseRegexPackageMatchProtocol[str]"], str],
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
            self: "BaseRegexPackagePatternProtocol[bytes]",
            repl: Union[
                ReadableBuffer,
                Callable[
                    ["BaseRegexPackageMatchProtocol[bytes]"],
                    ReadableBuffer
                ]
            ],
            string: ReadableBuffer,
            count: int = ...,
            flags: int = ...,
            pos: int | None = ...,
            endpos: int | None = ...,
            concurrent: bool | None = ...,
            timeout: float | None = ...,
    ) -> tuple[bytes, int]: ...

    @overload
    def subfn(
            self: "BaseRegexPackagePatternProtocol[str]",
            format: str | Callable[["BaseRegexPackageMatchProtocol[str]"], str],
            string: str,
            count: int = ...,
            flags: int = ...,
            pos: int | None = ...,
            endpos: int | None = ...,
            concurrent: bool | None = ...,
            timeout: float | None = ...,
    ) -> tuple[str, int]: ...

    @overload
    def subfn(
            self: "BaseRegexPackagePatternProtocol[bytes]",
            format: Union[
                ReadableBuffer,
                Callable[
                    ["BaseRegexPackageMatchProtocol[bytes]"],
                    ReadableBuffer]
            ],
            string: ReadableBuffer,
            count: int = ...,
            flags: int = ...,
            pos: int | None = ...,
            endpos: int | None = ...,
            concurrent: bool | None = ...,
            timeout: float | None = ...,
    ) -> tuple[bytes, int]: ...

    @overload
    def scanner(
            self: "BaseRegexPackagePatternProtocol[str]",
            string: str,
            pos: int | None = ...,
            endpos: int | None = ...,
            overlapped: bool = ...,
            concurrent: bool | None = ...,
            timeout: float | None = ...,
    ) -> "BaseRegexPackageScannerProtocol[str]": ...

    @overload
    def scanner(
            self: "BaseRegexPackagePatternProtocol[bytes]",
            string: bytes,
            pos: int | None = ...,
            endpos: int | None = ...,
            overlapped: bool = ...,
            concurrent: bool | None = ...,
            timeout: float | None = ...,
    ) -> "BaseRegexPackageScannerProtocol[bytes]": ...

    def __copy__(self) -> Self: ...

    def __deepcopy__(self) -> Self: ...

    if sys.version_info >= (3, 9):
        def __class_getitem__(cls, item: Any) -> GenericAlias: ...


@runtime_checkable
class BaseRegexPackageMatchProtocol(Protocol[AnyStr]):
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
class BaseSplitterProtocol(Protocol[AnyStr]):
    def __iter__(self) -> Self: ...

    def __next__(self) -> AnyStr | Any: ...

    def split(self) -> AnyStr | Any: ...


@runtime_checkable
class BaseRegexPackageScannerProtocol(Protocol[AnyStr]):
    def __iter__(self) -> Self: ...

    def __next__(self) -> BaseRegexPackageMatchProtocol[AnyStr]: ...

    def match(self) -> Optional[BaseRegexPackageMatchProtocol[AnyStr]]: ...

    def search(self) -> Optional[BaseRegexPackageMatchProtocol[AnyStr]]: ...
