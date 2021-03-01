from __future__ import annotations

from typing import Sequence, Type

from ._alphabet import Alphabet
from ._cdata import CData
from ._ffi import ffi, lib
from ._lprob import lprob_is_valid
from .build_ext import imm_float


class AlphabetLprob:
    """
    Alphabet log-probabilities.

    Parameters
    ----------
    imm_abc_lprob
        Alphabet log-probabilities.
    alphabet
        Alphabet.
    """

    def __init__(self, imm_abc_lprob: CData, alphabet: Alphabet):
        self._imm_abc_lprob = imm_abc_lprob
        if self._imm_abc_lprob == ffi.NULL:
            raise RuntimeError("`imm_abc_lprob` is NULL.")
        self._alphabet = alphabet

    @classmethod
    def create(
        cls: Type[AlphabetLprob], alphabet: Alphabet, lprobs: Sequence[float]
    ) -> AlphabetLprob:
        """
        Create an alphabet log-probabilities.

        Parameters
        ----------
        alphabet
            Alphabet.
        lprobs
            Log probability of each nucleotide.
        """
        imm_abc_lprob = lib.imm_abc_lprob_create(
            alphabet.imm_abc, ffi.new(f"{imm_float}[]", lprobs)
        )
        return cls(imm_abc_lprob, alphabet)

    @property
    def alphabet(self) -> Alphabet:
        return self._alphabet

    @property
    def imm_abc_lprob(self) -> CData:
        return self._imm_abc_lprob

    def lprob(self, symbol: bytes) -> float:
        lprob: float = lib.imm_abc_lprob_get(self._imm_abc_lprob, symbol)
        if not lprob_is_valid(lprob):
            raise RuntimeError("Could not get probability.")
        return lprob

    def __del__(self):
        if self._imm_abc_lprob != ffi.NULL:
            lib.imm_abc_lprob_destroy(self._imm_abc_lprob)
