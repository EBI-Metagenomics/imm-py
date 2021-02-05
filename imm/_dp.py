from typing import Generic, TypeVar

from . import wrap
from ._cdata import CData
from ._dp_task import DPTask
from ._ffi import ffi, lib
from ._hmm import HMM
from ._results import Results
from ._state import State

__all__ = ["DP"]

T = TypeVar("T", bound=State)


class DP(Generic[T]):
    def __init__(self, imm_dp: CData, hmm: HMM[T]):
        if imm_dp == ffi.NULL:
            raise RuntimeError("`imm_dp` is NULL.")
        self._imm_dp = imm_dp
        self._hmm = hmm

    @property
    def imm_dp(self) -> CData:
        return self._imm_dp

    def viterbi(self, task: DPTask) -> Results[T]:
        imm_results = lib.imm_dp_viterbi(self._imm_dp, task.imm_dp_task)
        if imm_results == ffi.NULL:
            raise RuntimeError("Could not run viterbi.")

        return wrap.imm_results(imm_results, task.sequence, self._hmm.states())

    def __del__(self):
        if self._imm_dp != ffi.NULL:
            lib.imm_dp_destroy(self._imm_dp)
