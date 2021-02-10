from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Type

from ._cdata import CData
from ._ffi import ffi, lib
from ._sequence import Sequence

if TYPE_CHECKING:
    from ._dp import DP


__all__ = ["DPTask"]


class DPTask:
    """
    DP task.

    Parameters
    ----------
    imm_dp_task
        DP task.
    """

    def __init__(self, imm_dp_task: CData):
        self._sequence: Optional[Sequence] = None
        if imm_dp_task == ffi.NULL:
            raise RuntimeError("`imm_dp_task` is NULL.")
        self._imm_dp_task = imm_dp_task

    @classmethod
    def create(cls: Type[DPTask], dp: DP) -> DPTask:
        """
        Create an DP task.

        Parameters
        ----------
        dp
            DP task.
        """
        return cls(lib.imm_dp_task_create(dp.imm_dp))

    def setup(self, seq: Sequence, window_length: int = 0):
        self._sequence = seq
        return lib.imm_dp_task_setup(self._imm_dp_task, seq.imm_seq, window_length)

    @property
    def sequence(self) -> Sequence:
        if self._sequence is None:
            raise RuntimeError("Sequence is None.")
        return self._sequence

    @property
    def imm_dp_task(self) -> CData:
        return self._imm_dp_task

    def __del__(self):
        if self._imm_dp_task != ffi.NULL:
            lib.imm_dp_task_destroy(self._imm_dp_task)
