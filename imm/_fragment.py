from typing import Iterator, TypeVar

from returns.primitives.hkt import SupportsKind2
from ._alphabet import Alphabet
from ._interval import Interval
from ._path import Path
from ._sequence import SequenceABC
from ._state import State
from ._step import Step

__all__ = ["FragStep", "Fragment"]

A = TypeVar("A", bound=Alphabet)
T = TypeVar("T", bound=State)


class FragStep(SupportsKind2["FragStep", A, T]):
    def __init__(self, sequence: SequenceABC[A], step: Step[A, T]):
        self._sequence = sequence
        self._step = step

    @property
    def sequence(self) -> SequenceABC[A]:
        return self._sequence

    @property
    def step(self) -> Step[A, T]:
        return self._step

    def __str__(self) -> str:
        return f"{str(self.sequence), str(self.step)}"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}:{str(self)}>"


class Fragment(SupportsKind2["Fragment", A, T]):
    """
    Fragment of a sequence.

    Parameters
    ----------
    sequence
        Sequence.
    path
        Path of the standard profile.
    """

    def __init__(
        self,
        sequence: SequenceABC[A],
        path: Path[A, T],
    ):
        self._sequence = sequence
        self._path = path

    @property
    def sequence(self) -> SequenceABC[A]:
        return self._sequence

    @property
    def path(self) -> Path[A, T]:
        return self._path

    def __iter__(self) -> Iterator[FragStep]:
        start = end = 0
        for step in self._path:
            end += step.seq_len
            yield FragStep(self._sequence[Interval(start, end)], step)
            start = end

    def __str__(self) -> str:
        return ",".join(str(seq_step) for seq_step in self)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}:{str(self)}>"
