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

def test():
# Example CMA for Lfd(a)
    Q = {'q0', 'qa', 'qb'}
    E = {'a', 'b'}
    T = {
        ('q0', 'a', '-'): {'qa'},
        ('qa', 'a', '-'): {'qa'},
        ('qb', 'a', '-'): {'qa'},

        ('q0', 'b', '-'): {'qb'},
        ('qa', 'b', '-'): {'qb'},
        ('qb', 'b', '-'): {'qb'},

        ('q0', 'b', 'qa'): {'qa'},
        ('qa', 'b', 'qa'): {'qa'},
        ('qb', 'b', 'qa'): {'qa'},

        ('q0', 'b', 'qb'): {'qb'},
        ('qa', 'b', 'qb'): {'qb'},
        ('qb', 'b', 'qb'): {'qb'},

        ('q0', 'a', 'qb'): {'qa'},
        ('qa', 'a', 'qb'): {'qa'},
        ('qb', 'a', 'qb'): {'qa'},
    }

    q0 = 'q0'
    Fl = {'q0', 'qa', 'qb'}
    Fg = {'q0', 'qa', 'qb'}

    cma = CMA(Q, E, T, q0, Fl, Fg)

    # Example test case:
    input_seq = [('a', 1), ('b', 2), ('a', 2), ('b', 2)]
    print("Accepted" if cma.accepts(input_seq) else "Rejected")


def parse_cma(filepath):
    with open(file_path, 'r') as f:
        content = f.read()

    namespace = {}
    exec(content, {}, namespace)

    Q = set(namespace['Q'])
    E = set(namespace['E'])
    q0 = namespace['q0']
    Fl = set(namespace['Fl'])
    Fg = set(namespace['Fg'])
    T = list(namespace['T'])    
    test_cases = list(namespace['test_cases'])

    return Q, E, T, q0, Fl, Fg, test_cases


file_path = r"C:\Users\hp\OneDrive\Desktop\Automata Tools\CMA\cma__1.txt"
Q, E, T, q0, Fl, Fg, test_case = parse_cma(file_path)

M = CMA(Q, E, T, q0, Fl, Fg)
for i, test in enumerate(test_case):
    result = M.accepts(test)
    print(f"Test case {i+1} accepted? {result}")


# test()