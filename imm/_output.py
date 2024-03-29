from __future__ import annotations

from typing import Type

from ._cdata import CData
from ._ffi import ffi, lib
from ._profile import Profile

__all__ = ["Output"]


class Output:
    """
    IMM file writer.

    Parameters
    ----------
    imm_output
        Output pointer.
    """

    def __init__(self, imm_output: CData):
        self._imm_output = imm_output
        if self._imm_output == ffi.NULL:
            raise RuntimeError("`imm_output` is NULL.")

    @classmethod
    def create(cls: Type[Output], filepath: bytes) -> Output:
        return cls(lib.imm_output_create(filepath))

    def write(self, profile: Profile):
        err: int = lib.imm_output_write(self._imm_output, profile.imm_profile)
        if err != 0:
            raise RuntimeError("Could not write profile.")

    def close(self):
        err: int = lib.imm_output_close(self._imm_output)
        if err != 0:
            raise RuntimeError("Could not close output.")

    def __del__(self):
        if self._imm_output != ffi.NULL:
            self.close()
            lib.imm_output_destroy(self._imm_output)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        del exception_type
        del exception_value
        del traceback
        self.close()
