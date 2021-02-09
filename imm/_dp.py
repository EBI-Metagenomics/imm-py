from typing import Generic, TypeVar

from . import wrap
from ._alphabet import Alphabet
from ._cdata import CData
from ._dp_task import DPTask
from ._ffi import ffi, lib
from ._hmm import HMM
from ._results import Results
from ._state import State

__all__ = ["DP"]

A = TypeVar("A", bound=Alphabet)
T = TypeVar("T", bound=State)


class DP(Generic[A, T]):
    def __init__(self, imm_dp: CData, hmm: HMM[A, T]):
        if imm_dp == ffi.NULL:
            raise RuntimeError("`imm_dp` is NULL.")
        self._imm_dp = imm_dp
        self._hmm = hmm

    @property
    def imm_dp(self) -> CData:
        return self._imm_dp

    def viterbi(self, task: DPTask[A, T]) -> Results[A, T]:
        imm_results = lib.imm_dp_viterbi(self._imm_dp, task.imm_dp_task)
        if imm_results == ffi.NULL:
            raise RuntimeError("Could not run viterbi.")
        states = self._hmm.states()
        return wrap.imm_results(imm_results, task.sequence, states)

    def __del__(self):
        if self._imm_dp != ffi.NULL:
            lib.imm_dp_destroy(self._imm_dp)
