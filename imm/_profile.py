from __future__ import annotations

from typing import List, Type

from ._alphabet import Alphabet
from ._cdata import CData
from ._ffi import ffi, lib
from ._model import Model

__all__ = ["Profile"]


class Profile:
    def __init__(self, imm_profile: CData, alphabet: Alphabet):
        self._imm_profile = ffi.NULL
        if imm_profile == ffi.NULL:
            raise RuntimeError("`imm_profile` is NULL.")
        self._models: List[Model] = []
        self._imm_profile = imm_profile
        self._alphabet = alphabet

    @property
    def alphabet(self) -> Alphabet:
        return self._alphabet

    def append_model(self, model: Model):
        lib.imm_profile_append_model(self._imm_profile, model.imm_model)
        self._models.append(model)

    @property
    def imm_profile(self) -> CData:
        return self._imm_profile

    @property
    def models(self):
        return self._models

    @classmethod
    def create(cls: Type[Profile], alphabet: Alphabet) -> Profile:
        return cls(lib.imm_profile_create(alphabet.imm_abc), alphabet)

    def __del__(self):
        if self._imm_profile != ffi.NULL:
            lib.imm_profile_free(self._imm_profile)
