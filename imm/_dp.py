from . import wrap
from ._cdata import CData
from ._dp_task import DPTask
from ._ffi import ffi, lib
from ._hmm import HMM
from ._result import Result

__all__ = ["DP"]


class DP:
    def __init__(self, imm_dp: CData, hmm: HMM):
        self._imm_dp = ffi.NULL
        if imm_dp == ffi.NULL:
            raise RuntimeError("`imm_dp` is NULL.")
        self._imm_dp = imm_dp
        self._hmm = hmm

    @property
    def imm_dp(self) -> CData:
        return self._imm_dp

    def viterbi(self, task: DPTask) -> Result:
        imm_result = lib.imm_dp_viterbi(self._imm_dp, task.imm_dp_task)
        if imm_result == ffi.NULL:
            raise RuntimeError("Could not run viterbi.")
        states = self._hmm.states()
        return wrap.imm_result(imm_result, task.sequence, states)

    def __del__(self):
        if self._imm_dp != ffi.NULL:
            lib.imm_dp_destroy(self._imm_dp)
