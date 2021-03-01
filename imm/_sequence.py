from __future__ import annotations

from typing import Optional, Type, Union

from ._alphabet import Alphabet
from ._cdata import CData
from ._ffi import ffi, lib
from ._interval import Interval

__all__ = ["Sequence"]


class Sequence:
    """
    Sequence of symbols from a given alphabet.

    Parameters
    ----------
    imm_seq
        Sequence pointer.
    alphabet
        Alphabet.
    """

    def __init__(
        self, imm_seq: CData, alphabet: Alphabet, parent: Optional[Sequence] = None
    ):
        self._parent = parent
        self._imm_seq = imm_seq
        if self._imm_seq == ffi.NULL:
            raise RuntimeError("`imm_seq` is NULL.")
        self._alphabet = alphabet

    @classmethod
    def create(cls: Type[Sequence], sequence: bytes, alphabet: Alphabet) -> Sequence:
        """
        Create a sequence of symbols.

        Parameters
        ----------
        sequence
            Sequence of symbols.
        alphabet
            Alphabet.
        """
        return cls(lib.imm_seq_create(sequence, alphabet.imm_abc), alphabet)

    def subseq(self, interval: Interval):
        """
        Subsequence of symbols of a given sequence.

        Parameters
        ----------
        interval
            Interval.
        """
        length = interval.stop - interval.start
        if interval.start < 0 or length < 0 or length > len(self):
            raise ValueError("Out-of-range interval.")

        imm_seq = ffi.new("struct imm_seq*")
        lib.imm_subseq_set(imm_seq, self.imm_seq, interval.start, length)
        return Sequence(imm_seq, self.alphabet, parent=self)

    @property
    def imm_seq(self) -> CData:
        return self._imm_seq

    def __len__(self) -> int:
        return lib.imm_seq_length(self._imm_seq)

    def __bytes__(self) -> bytes:
        length = lib.imm_seq_length(self._imm_seq)
        return ffi.string(lib.imm_seq_string(self._imm_seq), length)

    def __getitem__(self, i: Union[int, slice, Interval]) -> Union[bytes, Sequence]:
        if isinstance(i, int):
            return bytes(self)[i : i + 1]
        if isinstance(i, slice):
            interval = Interval.from_slice(i)
        elif isinstance(i, Interval):
            interval = i
        else:
            raise RuntimeError("Index has to be an integer of a slice.")

        return self.subseq(interval)

    @property
    def alphabet(self) -> Alphabet:
        return self._alphabet

    def __del__(self):
        if self._imm_seq != ffi.NULL:
            if self._parent is None:
                lib.imm_seq_destroy(self._imm_seq)

    def __str__(self) -> str:
        return f"{bytes(self).decode()}"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}:{str(self)}>"
