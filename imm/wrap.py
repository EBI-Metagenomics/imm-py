from __future__ import annotations

from typing import List, Mapping, TypeVar

from ._alphabet import Alphabet
from ._cdata import CData
from ._ffi import ffi, lib
from ._path import Path
from ._result import Result
from ._results import Results
from ._sequence import Sequence, SubSequence
from ._state import MuteState, NormalState, State, StateType, TableState
from ._step import Step

A = TypeVar("A", bound=Alphabet)
S = TypeVar("S", bound=State)


def wrap_imm_state(imm_state: CData, alphabet: A) -> State:
    state_type = StateType(lib.imm_state_type_id(imm_state))
    if state_type == StateType.MUTE:
        return MuteState(lib.imm_mute_state_derived(imm_state), alphabet)
    if state_type == StateType.NORMAL:
        return NormalState(lib.imm_normal_state_derived(imm_state), alphabet)
    if state_type == StateType.TABLE:
        return TableState(lib.imm_table_state_derived(imm_state), alphabet)
    raise ValueError(f"Unknown state type: {state_type}.")


def wrap_imm_results(imm_results: CData, sequence: Sequence, states: Mapping[CData, S]):
    results: List[Result[S]] = []
    for i in range(lib.imm_results_size(imm_results)):
        imm_result = lib.imm_results_get(imm_results, i)
        results.append(wrap_imm_result(imm_result, sequence, states))

    return Results(imm_results, results, sequence)


def wrap_imm_result(imm_result: CData, sequence: Sequence, states: Mapping[CData, S]):
    path = wrap_imm_path(lib.imm_result_path(imm_result), states)
    imm_subseq = lib.imm_result_subseq(imm_result)
    return Result(imm_result, path, SubSequence(imm_subseq, sequence))


def wrap_imm_path(imm_path: CData, states: Mapping[CData, S]) -> Path:
    steps: List[Step[S]] = []
    imm_step = lib.imm_path_first(imm_path)
    while imm_step != ffi.NULL:
        imm_state = lib.imm_step_state(imm_step)
        steps.append(Step(imm_step, states[imm_state]))
        imm_step = lib.imm_path_next(imm_path, imm_step)

    return Path(imm_path, steps)
