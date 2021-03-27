from typing import BinaryIO, Callable, Optional as _Optional

from .core import Construct, Subconstruct, _ContextContainer

class Probe(Construct):
    flagbuildnone: bool = ...
    into: _Optional[Callable[[_ContextContainer], None]] = ...
    lookahead: _Optional[int] = ...
    def __init__(self, into: _Optional[Callable[[_ContextContainer], None]] = ..., lookahead: _Optional[int] = ...) -> None: ...
    def printout(self, stream: BinaryIO, context: _ContextContainer, path: _Optional[str]) -> None: ...

class Debugger(Subconstruct):
    def handle_exc(self, path: _Optional[str], msg: _Optional[str] = ...) -> None: ...
