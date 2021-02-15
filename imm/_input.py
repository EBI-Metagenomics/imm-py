from __future__ import annotations

from typing import Iterator, Type

from . import wrap
from ._cdata import CData
from ._dp import DP
from ._ffi import ffi, lib
from ._hmm import HMM
from ._hmm_block import HMMBlock
from ._model import Model

__all__ = ["Input"]


class Input:
    """
    IMM file reader.

    Parameters
    ----------
    imm_input
        Input pointer.
    """

    def __init__(self, imm_input: CData):
        if imm_input == ffi.NULL:
            raise RuntimeError("`imm_input` is NULL.")
        self._imm_input = imm_input

    @classmethod
    def create(cls: Type[Input], filepath: bytes) -> Input:
        return cls(lib.imm_input_create(filepath))

    def read(self) -> Model:
        imm_model = lib.imm_input_read(self._imm_input)
        if imm_model == ffi.NULL:
            if lib.imm_input_eof(self._imm_input):
                raise StopIteration
            raise RuntimeError("Could not read model.")

        abc = wrap.imm_abc(lib.imm_model_abc(imm_model))

        model = Model(imm_model, abc)
        for i in range(lib.imm_model_nhmm_blocks(imm_model)):
            imm_hmm_block = lib.imm_model_get_hmm_block(imm_model, i)
            states = {}
            for j in range(lib.imm_hmm_block_nstates(imm_hmm_block)):
                imm_state = lib.imm_hmm_block_state(imm_hmm_block, j)
                states[imm_state] = wrap.imm_state(imm_state, abc)

            hmm = HMM(lib.imm_hmm_block_hmm(imm_hmm_block), abc, states)
            dp = DP(lib.imm_hmm_block_dp(imm_hmm_block), hmm)
            hmm_block = HMMBlock(imm_hmm_block, hmm, dp)
            model.append_hmm_block(hmm_block)
        return model

    def close(self):
        err: int = lib.imm_input_close(self._imm_input)
        if err != 0:
            raise RuntimeError("Could not close input.")

    def __del__(self):
        if self._imm_input != ffi.NULL:
            lib.imm_input_destroy(self._imm_input)

    def __iter__(self) -> Iterator[Model]:
        while True:
            try:
                yield self.read()
            except StopIteration:
                return

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        del exception_type
        del exception_value
        del traceback
        self.close()
