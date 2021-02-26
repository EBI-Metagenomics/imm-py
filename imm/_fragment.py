from ._interval import Interval
from ._path import Path
from ._sequence import Sequence
from ._step import Step

__all__ = ["FragStep", "Fragment"]


class FragStep:
    def __init__(self, sequence: Sequence, step: Step):
        self._sequence = sequence
        self._step = step

    @property
    def sequence(self) -> Sequence:
        return self._sequence

    @property
    def step(self) -> Step:
        return self._step

    def __str__(self) -> str:
        return f"{str(self.sequence), str(self.step)}"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}:{str(self)}>"


class Fragment:
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
        sequence: Sequence,
        path: Path,
    ):
        self._sequence = sequence
        self._path = path

    @property
    def sequence(self) -> Sequence:
        return self._sequence

    @property
    def path(self) -> Path:
        return self._path

    def __iter__(self):
        start = end = 0
        for step in self._path:
            end += step.seq_len
            yield FragStep(self._sequence[Interval(start, end)], step)
            start = end

    def __str__(self) -> str:
        return ",".join(str(seq_step) for seq_step in self)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}:{str(self)}>"
