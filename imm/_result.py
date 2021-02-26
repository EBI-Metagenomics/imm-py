from ._cdata import CData
from ._ffi import ffi, lib
from ._path import Path
from ._sequence import Sequence

__all__ = ["Result"]


class Result:
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
        path: Path,
        sequence: Sequence,
    ):
        self._imm_result = ffi.NULL
        if imm_result == ffi.NULL:
            raise RuntimeError("`imm_result` is NULL.")
        self._imm_result = imm_result
        self._path = path
        self._sequence = sequence

    @property
    def path(self) -> Path:
        return self._path

    @property
    def sequence(self) -> Sequence:
        return self._sequence

    def __del__(self):
        if self._imm_result != ffi.NULL:
            lib.imm_result_free(self._imm_result)
