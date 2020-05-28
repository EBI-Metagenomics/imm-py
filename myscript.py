from math import log

from imm import HMM, Alphabet, MuteState, NormalState, lprob_zero

alphabet = Alphabet.create(b"ACGU", b"X")
hmm = HMM.create(alphabet)

S = MuteState.create(b"S", alphabet)
hmm.add_state(S, log(1.0))

E = MuteState.create(b"E", alphabet)
hmm.add_state(E, lprob_zero())

M1 = NormalState.create(
    b"M1", alphabet, [log(0.8), log(0.2), lprob_zero(), lprob_zero()],
)
hmm.add_state(M1, lprob_zero())

M2 = NormalState.create(
    b"M2", alphabet, [log(0.4 / 1.6), log(0.6 / 1.6), lprob_zero(), log(0.6 / 1.6)]
)
hmm.add_state(M2, lprob_zero())

hmm.set_transition(S, M1, log(1.0))
hmm.set_transition(M1, M2, log(1.0))
hmm.set_transition(M2, E, log(1.0))
hmm.set_transition(E, E, log(1.0))
hmm.normalize()
print(hmm)
