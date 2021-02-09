from __future__ import annotations

from typing import Generic, Type, TypeVar

from ._alphabet import Alphabet
from ._cdata import CData
from ._dp import DP
from ._ffi import ffi, lib
from ._hmm import HMM
from ._state import State

__all__ = ["Model"]


A = TypeVar("A", bound=Alphabet)
T = TypeVar("T", bound=State)


class Model(Generic[A, T]):
    def __init__(self, imm_model: CData, hmm: HMM[A, T], dp: DP[A, T]):
        if imm_model == ffi.NULL:
            raise RuntimeError("`imm_model` is NULL.")
        self._imm_model = imm_model
        self._hmm = hmm
        self._dp = dp

    @property
    def imm_model(self) -> CData:
        return self._imm_model

    @classmethod
    def create(cls: Type[Model[A, T]], hmm: HMM[A, T], dp: DP[A, T]) -> Model[A, T]:
        return cls(lib.imm_model_create(hmm.imm_hmm, dp.imm_dp), hmm, dp)

    @property
    def alphabet(self) -> Alphabet:
        return self._hmm.alphabet

    @property
    def dp(self) -> DP[A, T]:
        return self._dp

    @property
    def hmm(self) -> HMM[A, T]:
        return self._hmm

    def __del__(self):
        if self._imm_model != ffi.NULL:
            lib.imm_model_destroy(self._imm_model)
