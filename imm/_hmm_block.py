from __future__ import annotations

from typing import Type

from ._cdata import CData
from ._dp import DP
from ._ffi import ffi, lib
from ._hmm import HMM

__all__ = ["HMMBlock"]


class HMMBlock:
    def __init__(self, imm_hmm_block: CData, hmm: HMM, dp: DP):
        self._imm_hmm_block = ffi.NULL
        if imm_hmm_block == ffi.NULL:
            raise RuntimeError("`imm_hmm_block` is NULL.")
        self._imm_hmm_block = imm_hmm_block
        self._hmm = hmm
        self._dp = dp

    @property
    def imm_hmm_block(self) -> CData:
        return self._imm_hmm_block

    @classmethod
    def create(cls: Type[HMMBlock], hmm: HMM, dp: DP) -> HMMBlock:
        return cls(lib.imm_hmm_block_create(hmm.imm_hmm, dp.imm_dp), hmm, dp)

    @property
    def hmm(self) -> HMM:
        return self._hmm

    @property
    def dp(self) -> DP:
        return self._dp
