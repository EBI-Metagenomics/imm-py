from __future__ import annotations

from typing import List, Mapping

from ._alphabet import Alphabet, AlphabetType
from ._cdata import CData
from ._ffi import ffi, lib
from ._interval import Interval
from ._path import Path
from ._result import Result
from ._sequence import Sequence
from ._state import MuteState, NormalState, State, StateType, TableState
from ._step import Step

__all__ = ["imm_abc", "imm_path", "imm_result", "imm_state"]


def imm_abc(ptr: CData):
    alphabet_type = AlphabetType(lib.imm_abc_type_id(ptr))
    assert alphabet_type == AlphabetType.ABC
    return Alphabet(ptr)


def imm_path(ptr: CData, states: Mapping[CData, State]) -> Path:
    steps: List[Step] = []
    imm_step = lib.imm_path_first(ptr)
    while imm_step != ffi.NULL:
        imm_state = lib.imm_step_state(imm_step)
        state = states[imm_state]
        steps.append(Step(imm_step, state))
        imm_step = lib.imm_path_next(ptr, imm_step)

    return Path(ptr, steps)


def imm_result(imm_result: CData, sequence: Sequence, states: Mapping[CData, State]):
    path = imm_path(lib.imm_result_path(imm_result), states)
    return Result(imm_result, path, sequence.subseq(Interval(0, len(sequence))))


def imm_state(ptr: CData, alphabet: Alphabet) -> State:
    state_type = StateType(lib.imm_state_type_id(ptr))
    if state_type == StateType.MUTE:
        return MuteState(lib.imm_mute_state_derived(ptr), alphabet)
    if state_type == StateType.NORMAL:
        return NormalState(lib.imm_normal_state_derived(ptr), alphabet)
    if state_type == StateType.TABLE:
        return TableState(lib.imm_table_state_derived(ptr), alphabet)
    raise ValueError(f"Unknown state type: {state_type}.")
