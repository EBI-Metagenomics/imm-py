from __future__ import annotations

from typing import Iterable, Iterator, Type

from ._cdata import CData
from ._ffi import ffi, lib
from ._step import Step

__all__ = ["Path"]


class Path:
    """
    Path.

    Parameters
    ----------
    imm_path
        Path pointer.
    steps
        Steps.
    """

    def __init__(self, imm_path: CData, steps: Iterable[Step]):
        self._imm_path = imm_path
        if self._imm_path == ffi.NULL:
            raise RuntimeError("`imm_path` is NULL.")
        self._steps = list(steps)

    @classmethod
    def create(cls: Type[Path], steps: Iterable[Step]) -> Path:
        """
        Create path.

        Parameters
        ----------
        steps
            Steps.
        """
        imm_path = lib.imm_path_create()
        for step in steps:
            lib.imm_path_append(imm_path, step.imm_step)
        return cls(imm_path, list(steps))

    @property
    def imm_path(self) -> CData:
        return self._imm_path

    def __len__(self) -> int:
        return len(self._steps)

    def __getitem__(self, i: int) -> Step:
        return self._steps[i]

    def __iter__(self) -> Iterator[Step]:
        for i in range(len(self)):
            yield self[i]

    def __del__(self):
        if self._imm_path != ffi.NULL:
            lib.imm_path_free(self._imm_path)

    def __str__(self) -> str:
        return ",".join([str(s) for s in self])

    def __repr__(self):
        return f"<{self.__class__.__name__}:{str(self)}>"
