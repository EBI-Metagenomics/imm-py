from ._alphabet import Alphabet
from ._alphabet_table import AlphabetTable
from ._dp import DP
from ._fragment import Fragment, FragStep
from ._hmm import HMM
from ._lprob import (
    lprob_invalid,
    lprob_is_valid,
    lprob_is_zero,
    lprob_normalize,
    lprob_zero,
)
from ._path import Path
from ._result import Result
from ._results import Results
from ._sequence import Sequence, SequenceABC, SubSequence
from ._sequence_table import SequenceTable
from ._state import MuteState, NormalState, State, StateType, TableState, wrap_imm_state
from ._step import Step

try:
    from ._ffi import ffi

    del ffi
except Exception as e:
    _ffi_err = """
It is likely caused by a broken installation of this package.
Please, make sure you have a C compiler and try to uninstall
and reinstall the package again."""

    raise RuntimeError(str(e) + _ffi_err)

__version__ = "0.0.1"


__all__ = [
    "Alphabet",
    "AlphabetTable",
    "DP",
    "FragStep",
    "Fragment",
    "HMM",
    "MuteState",
    "NormalState",
    "Path",
    "Result",
    "Results",
    "Sequence",
    "SequenceABC",
    "SequenceTable",
    "State",
    "StateType",
    "Step",
    "SubSequence",
    "TableState",
    "lprob_invalid",
    "lprob_is_valid",
    "lprob_is_zero",
    "lprob_normalize",
    "lprob_zero",
    "wrap_imm_state",
]
