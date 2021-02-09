from typing import Generic, TypeVar

from ._alphabet import Alphabet
from ._cdata import CData
from ._ffi import ffi, lib
from ._path import Path
from ._sequence import SubSequence
from ._state import State

__all__ = ["Result"]

A = TypeVar("A", bound=Alphabet)
T = TypeVar("T", bound=State)


class Result(Generic[A, T]):
    """
    Result.

    Parameters
    ----------
    imm_result
        Result pointer.
    path
        Path.
    sequence
        Sequence.
    """

    def __init__(
        self,
        imm_result: CData,
        path: Path[A, T],
        sequence: SubSequence[A],
    ):
        if imm_result == ffi.NULL:
            raise RuntimeError("`imm_result` is NULL.")
        self._imm_result = imm_result
        self._path = path
        self._sequence = sequence

    @property
    def path(self) -> Path[A, T]:
        return self._path

    @property
    def sequence(self) -> SubSequence[A]:
        return self._sequence

    def __del__(self):
        if self._imm_result != ffi.NULL:
            lib.imm_result_free(self._imm_result)
