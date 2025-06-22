from typing import List, Tuple, Dict
from collections import deque


class RA:
    def __init__(self, Q, E, T, R0, U, q0, F, k):

        self.Q = Q
        self.E = E
        self.T = self.convert(T)  # Transitions: (q, a, i) → q'
        self.R = R0  # Current register config: [k] → D⊥
        self.U = U  # Update function: (q, a) → j
        self.q0 = q0
        self.F = F
        self.k = k

    def convert(self,T):
        CT = {}
        for state, symbol, condition, next_states in T:
            key = (state, symbol, condition)
            if key in CT:
                CT[key] |= next_states  # Union the sets
            else:
                CT[key] = set(next_states)
        return CT

    def accepts(self, string: List[Tuple[str, str]]) -> bool:
        # current_states = {(self.q0, 0, frozenset((h, str(v)) for h, v in self.R.items()))}
        queue = deque()
        queue.append((self.q0, 0, frozenset((h, str(v)) for h, v in self.R.items())))
        while queue:
            state, pos, r_frozen = queue.popleft()
            r_cur = dict(r_frozen)

            if pos == len(string):
                if state in self.F:
                    return True
                continue

            a, d = string[pos]
            matched = False

            # Case 1: d matches existing register value
            for reg, val in r_cur.items():
                if val == d :
                    matched = True
                    if (state, a, reg) in self.T:
                        for next_state in self.T[(state, a, reg)]:
                            queue.append((next_state, pos + 1, r_frozen))  # No change to registers

            if matched:
                continue

            # Case 2: fresh value
            if (state, a) in self.U:
                j = self.U[(state, a)]
                r_next = dict(r_cur)
                r_next[j] = d
                if (state, a, j) in self.T:
                    for next_state in self.T[(state, a, j)]:
                        queue.append((next_state, pos + 1, frozenset(r_next.items())))
                            
        return False