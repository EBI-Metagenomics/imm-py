from math import log

import pytest
from numpy.testing import assert_allclose, assert_equal

from imm import Alphabet
from imm import SequenceTable, lprob_is_zero
from imm import Sequence
from imm import MuteState, NormalState, TableState


def test_normal_state():
    alphabet = Alphabet.create(b"ACGT", b"X")

    state = NormalState.create(
        b"M0", alphabet, [log(0.1), log(0.2), log(0.3), log(0.3)],
    )
    assert_equal(state.name, b"M0")
    assert_equal(state.lprob(Sequence.create(b"A", alphabet)), log(0.1))
    assert_equal(state.lprob(Sequence.create(b"C", alphabet)), log(0.2))
    assert_equal(state.lprob(Sequence.create(b"G", alphabet)), log(0.3))
    assert_equal(state.lprob(Sequence.create(b"T", alphabet)), log(0.3))
    assert_equal(state.min_seq, 1)
    assert_equal(state.max_seq, 1)

    with pytest.raises(RuntimeError):
        state.lprob(Sequence.create(b"T", Alphabet.create(b"ACGT", b"X")))

    assert_equal(lprob_is_zero(state.lprob(Sequence.create(b"AC", alphabet))), True)

    assert_equal(str(state), "M0")
    assert_equal(repr(state), "<NormalState:M0>")


def test_mute_state():
    alphabet = Alphabet.create(b"ACGU", b"X")
    state = MuteState.create(b"S", alphabet)

    assert_equal(state.name, b"S")
    assert_equal(state.lprob(Sequence.create(b"", alphabet)), log(1.0))
    assert_equal(lprob_is_zero(state.lprob(Sequence.create(b"AC", alphabet))), True)
    assert_equal(state.min_seq, 0)
    assert_equal(state.max_seq, 0)
    assert_equal(str(state), "S")
    assert_equal(repr(state), "<MuteState:S>")


def test_table_state():
    alphabet = Alphabet.create(b"ACGU", b"X")
    seqt = SequenceTable.create(alphabet)
    seqt.add(Sequence.create(b"AUG", alphabet), log(0.8))
    seqt.add(Sequence.create(b"AUU", alphabet), log(0.4))

    state = TableState.create(b"M2", seqt)
    assert_equal(state.name, b"M2")
    assert_allclose(state.lprob(Sequence.create(b"AUG", alphabet)), log(0.8))
    assert_allclose(state.lprob(Sequence.create(b"AUU", alphabet)), log(0.4))
    assert_equal(str(state), "M2")
    assert_equal(repr(state), "<TableState:M2>")
