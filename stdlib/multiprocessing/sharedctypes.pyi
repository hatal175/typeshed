import ctypes
from ctypes import _CData, _SimpleCData, c_char
from multiprocessing.context import BaseContext
from multiprocessing.synchronize import _LockLike
from typing import (
    Any,
    Callable,
    ContextManager,
    Generic,
    Iterable,
    List,
    Optional,
    Protocol,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
)
from typing_extensions import Literal

_T = TypeVar("_T")
_CT = TypeVar("_CT", bound=_CData)
@overload
def RawValue(typecode_or_type: Type[_CT], *args: Any) -> _CT: ...
@overload
def RawValue(typecode_or_type: Union[str, Type[_CData]], *args: Any) -> Any: ...
@overload
def RawArray(typecode_or_type: Type[_CT], size_or_initializer: Union[int, Sequence[Any]]) -> ctypes.Array[_CT]: ...
@overload
def RawArray(typecode_or_type: Union[str, Type[_CData]], size_or_initializer: Union[int, Sequence[Any]]) -> Any: ...
@overload
def Value(typecode_or_type: Type[_CT], *args: Any, lock: Literal[False], ctx: Optional[BaseContext] = ...) -> _CT: ...
@overload
def Value(
    typecode_or_type: Type[_CT],
    *args: Any,
    lock: Union[Literal[True], _LockLike],
    ctx: Optional[BaseContext] = ...,
) -> SynchronizedBase[_CT]: ...
@overload
def Value(
    typecode_or_type: Union[str, Type[_CData]],
    *args: Any,
    lock: Union[Literal[True], _LockLike],
    ctx: Optional[BaseContext] = ...,
) -> SynchronizedBase: ...
@overload
def Value(
    typecode_or_type: Union[str, Type[_CData]], *args: Any, lock: Union[bool, _LockLike] = ..., ctx: Optional[BaseContext] = ...
) -> Any: ...
@overload
def Array(
    typecode_or_type: Type[_CT],
    size_or_initializer: Union[int, Sequence[Any]],
    *,
    lock: Literal[False],
    ctx: Optional[BaseContext] = ...,
) -> _CT: ...
@overload
def Array(
    typecode_or_type: Type[_CT],
    size_or_initializer: Union[int, Sequence[Any]],
    *,
    lock: Union[Literal[True], _LockLike],
    ctx: Optional[BaseContext] = ...,
) -> SynchronizedArray[_CT]: ...
@overload
def Array(
    typecode_or_type: Union[str, Type[_CData]],
    size_or_initializer: Union[int, Sequence[Any]],
    *,
    lock: Union[Literal[True], _LockLike],
    ctx: Optional[BaseContext] = ...,
) -> SynchronizedArray: ...
@overload
def Array(
    typecode_or_type: Union[str, Type[_CData]],
    size_or_initializer: Union[int, Sequence[Any]],
    *,
    lock: Union[bool, _LockLike] = ...,
    ctx: Optional[BaseContext] = ...,
) -> Any: ...
def copy(obj: _CT) -> _CT: ...

_SimpleCDataT = TypeVar("_SimpleCDataT", bound=_SimpleCData)

# Could not make this overload work
# @overload
# def synchronized(obj: _SimpleCDataT, lock: Optional[_LockLike] = ..., ctx: Optional[Any] = ...) -> Synchronized[_SimpleCDataT]: ...
@overload
def synchronized(obj: ctypes.Array[c_char], lock: Optional[_LockLike] = ..., ctx: Optional[Any] = ...) -> SynchronizedString: ...
@overload
def synchronized(obj: ctypes.Array[_CT], lock: Optional[_LockLike] = ..., ctx: Optional[Any] = ...) -> SynchronizedArray[_CT]: ...
@overload
def synchronized(obj: _CT, lock: Optional[_LockLike] = ..., ctx: Optional[Any] = ...) -> SynchronizedBase[_CT]: ...

class _AcquireFunc(Protocol):
    def __call__(self, block: bool = ..., timeout: Optional[float] = ...) -> bool: ...

class SynchronizedBase(ContextManager[bool], Generic[_CT]):
    acquire: _AcquireFunc = ...
    release: Callable[[], None] = ...
    def __init__(self, obj: Any, lock: Optional[_LockLike] = ..., ctx: Optional[Any] = ...) -> None: ...
    def __reduce__(self) -> Tuple[Callable, Tuple[Any, _LockLike]]: ...
    def get_obj(self) -> _CT: ...
    def get_lock(self) -> _LockLike: ...

class Synchronized(SynchronizedBase[_SimpleCData[_T]], Generic[_T]):
    value: _T = ...

class SynchronizedArray(SynchronizedBase[ctypes.Array[_CT]], Generic[_CT]):
    def __len__(self) -> int: ...
    @overload
    def __getitem__(self, i: int) -> _CT: ...
    @overload
    def __getitem__(self, s: slice) -> List[_CT]: ...
    @overload
    def __setitem__(self, i: int, o: _CT) -> None: ...
    @overload
    def __setitem__(self, s: slice, o: Iterable[_CT]) -> None: ...
    def __getslice__(self, start: int, stop: int) -> List[_CT]: ...
    def __setslice__(self, start: int, stop: int, values: Iterable[_CT]) -> None: ...

class SynchronizedString(SynchronizedArray[c_char]):
    value: bytes = ...
    raw: bytes = ...
