from math import log
from pathlib import Path

import pytest

from imm import (
    HMM,
    Alphabet,
    DPTask,
    Input,
    Model,
    MuteState,
    NormalState,
    Output,
    Sequence,
    lprob_zero,
)
from imm.testing import assert_allclose


@pytest.fixture
def imm_example():
    alphabet = Alphabet.create(b"AC", b"X")
    hmm = HMM.create(alphabet)

    S = MuteState.create(b"S", alphabet)
    hmm.add_state(S, log(1.0))

    E = MuteState.create(b"E", alphabet)
    hmm.add_state(E, lprob_zero())

    M1 = NormalState.create(b"M1", alphabet, [log(0.8), log(0.2)])
    hmm.add_state(M1, lprob_zero())

    M2 = NormalState.create(b"M2", alphabet, [log(0.4), log(0.6)])
    hmm.add_state(M2, lprob_zero())

    hmm.set_transition(S, M1, log(1.0))
    hmm.set_transition(M1, M2, log(1.0))
    hmm.set_transition(M2, E, log(1.0))
    hmm.set_transition(E, E, log(1.0))
    hmm.normalize()
    hmm.set_transition(E, E, lprob_zero())

    dp = hmm.create_dp(E)

    return {"hmm": hmm, "dp": dp, "alphabet": alphabet}


def test_io(tmpdir, imm_example):
    alphabet = imm_example["alphabet"]
    hmm = imm_example["hmm"]
    dp = imm_example["dp"]

    dp_task = DPTask.create(dp)
    dp_task.setup(Sequence.create(b"AC", alphabet))
    r = dp.viterbi(dp_task)[0]
    assert_allclose(hmm.loglikelihood(r.sequence, r.path), log(0.48))

    filepath = Path(tmpdir / "model.imm")
    with Output.create(bytes(filepath)) as output:
        output.write(Model.create(hmm, dp))
        output.write(Model.create(hmm, dp))
        output.write(Model.create(hmm, dp))

    input = Input.create(bytes(filepath))
    nmodels = 0
    for model in input:
        alphabet = model.alphabet
        dp_task = DPTask.create(model.dp)
        dp_task.setup(Sequence.create(b"AC", alphabet))
        r = model.dp.viterbi(dp_task)[0]
        hmm = model.hmm
        assert_allclose(hmm.loglikelihood(r.sequence, r.path), log(0.48))
        nmodels += 1
    input.close()
    assert nmodels == 3

    with Input.create(bytes(filepath)) as input:
        nmodels = 0
        for model in input:
            alphabet = model.alphabet
            dp_task = DPTask.create(model.dp)
            dp_task.setup(Sequence.create(b"AC", alphabet))
            r = model.dp.viterbi(dp_task)[0]
            hmm = model.hmm
            assert_allclose(hmm.loglikelihood(r.sequence, r.path), log(0.48))
            nmodels += 1
        assert nmodels == 3
