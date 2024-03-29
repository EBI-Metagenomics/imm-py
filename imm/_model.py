from __future__ import annotations

from typing import Type

from ._cdata import CData
from ._dp import DP
from ._ffi import ffi, lib
from ._hmm import HMM

__all__ = ["Model"]


class Model:
    def __init__(self, imm_model: CData, hmm: HMM, dp: DP):
        self._imm_model = imm_model
        if self._imm_model == ffi.NULL:
            raise RuntimeError("`imm_model` is NULL.")
        self._hmm = hmm
        self._dp = dp

    @property
    def imm_model(self) -> CData:
        return self._imm_model

    @classmethod
    def create(cls: Type[Model], hmm: HMM, dp: DP) -> Model:
        return cls(lib.imm_model_create(hmm.imm_hmm, dp.imm_dp), hmm, dp)

    @property
    def hmm(self) -> HMM:
        return self._hmm

    @property
    def dp(self) -> DP:
        return self._dp

    def __del__(self):
        if self._imm_model != ffi.NULL:
            lib.imm_model_destroy(self._imm_model, False)
