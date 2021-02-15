from __future__ import annotations

from typing import List, Type

from ._alphabet import Alphabet
from ._cdata import CData
from ._ffi import ffi, lib
from ._hmm_block import HMMBlock

__all__ = ["Model"]


class Model:
    def __init__(self, imm_model: CData, alphabet: Alphabet):
        if imm_model == ffi.NULL:
            raise RuntimeError("`imm_model` is NULL.")
        self._hmm_blocks: List[HMMBlock] = []
        self._imm_model = imm_model
        self._alphabet = alphabet

    @property
    def alphabet(self) -> Alphabet:
        return self._alphabet

    def append_hmm_block(self, hmm_block: HMMBlock):
        lib.imm_model_append_hmm_block(self._imm_model, hmm_block.imm_hmm_block)
        self._hmm_blocks.append(hmm_block)

    @property
    def imm_model(self) -> CData:
        return self._imm_model

    @property
    def hmm_blocks(self):
        return self._hmm_blocks

    @classmethod
    def create(cls: Type[Model], alphabet: Alphabet) -> Model:
        return cls(lib.imm_model_create(alphabet.imm_abc), alphabet)

    def __del__(self):
        if self._imm_model != ffi.NULL:
            lib.imm_model_free(self._imm_model)
