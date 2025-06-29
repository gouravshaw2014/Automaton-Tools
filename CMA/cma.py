from collections import deque
from copy import deepcopy

class CMA:
    def __init__(self, Q, Sigma, delta, q0, Fl, Fg):
        self.Q = Q              # Set of states
        self.E = Sigma      # Alphabet
        self.T = self.convert(delta)      # Transition relation: (state, symbol, last_state) -> set of next states
        self.q0 = q0            # Initial state
        self.Fl = Fl            # Local accepting states
        self.Fg = Fg            # Global accepting states

    def convert(self, T):
        CT = {}
        for state, symbol,last_used, next_states in T:
            key = (state, symbol, last_used)
            if key in CT:
                CT[key] |= next_states  # Union the sets
            else:
                CT[key] = set(next_states)
        return CT

    def accepts(self, input_seq):
        queue = deque()
        h0 = {}  # hash function: data -> last used state, initially empty
        queue.append((self.q0, 0, h0))  # (current_state, input_index, hash_function)

        while queue:
            state, i, h = queue.popleft()

            if i == len(input_seq):
                # Global acceptance check
                if state in self.Fg and all(v in self.Fl for v in h.values()):
                    return True
                continue

            sym, data = input_seq[i]
            last_state = h.get(data, '-')  # '-' represents unseen (⊥)
            key = (state, sym, last_state)

            if key in self.T:
                for next_state in self.T[key]:
                    new_h = deepcopy(h)
                    new_h[data] = next_state  # update memory
                    queue.append((next_state, i + 1, new_h))

        return False