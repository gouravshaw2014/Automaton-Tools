from typing import List, Tuple, Dict, Set
from collections import deque

class SAFA:
    def __init__(self, Q: Set[str], E: Set[str], q0: str, F: Set[str],
                 H: Dict[str, Set[str]],
                 T: Dict[Tuple[str, str, str, str], Set[str]]):  # (state, symbol, condition, set_name) -> next_states
        self.Q = Q
        self.E = E
        self.q0 = q0
        self.F = F
        self.H = H
        self.T = T

    def accepts(self, w: List[Tuple[str, str]]) -> bool:
        initial_config = (self.q0, {h: set(v) for h, v in self.H.items()})
        queue = deque()
        queue.append((0, initial_config))  # (position, (state, H))

        while queue:
            pos, (state, H_copy) = queue.popleft()

            if pos == len(w):
                if state in self.F:
                    return True
                continue

            symbol, data = w[pos]

            for (q, a, cond, set_name), next_states in self.T.items():
                if q != state or a != symbol:
                    continue

                # If no set is used (e.g., set_name == '-'), we skip checking known/new
                if set_name != '-':
                    known = data in H_copy[set_name]

                    if cond == "0" and not known:
                        continue
                    if cond == "1" and known:
                        continue

                for q_next in next_states:
                    H_next = {h: set(s) for h, s in H_copy.items()}
                    if cond == "1" and set_name != '-':
                        H_next[set_name].add(data)

                    queue.append((pos + 1, (q_next, H_next)))

        return False

def a():
    Q = {'q0', 'q1'}
    E = {'a', 'b'}
    q0 = 'q0'
    F = {'q0'}
    H = {'h1': set()}

    # Transition function: (state, symbol, "0" for known / "1" for new, set_name) -> next_states
    T = {
        ('q0', 'a', '1', 'h1'): {'q0'},  # new value, insert into h1
        ('q0', 'a', '0', '-'): {'q1'},  # known value
        ('q1', 'b', '1', '-'): {'q0'},
        ('q1', 'b', '0', '-'): {'q0'},
    }

    M = SAFA(Q, E, q0, F, H, T)

    # Input: [('a', '1'), ('a', '2'), ('a', '3')]
    w = [('a', '1'), ('a', '2'), ('a', '1')]
    print("Accepted?", M.accepts(w))  # Should return True

def load_safa_from_pyfile(filepath):
    context = {}
    with open(filepath, 'r') as f:
        code = f.read()
    exec(code, {}, context)
    # Now context dict has Q, E, q0, F, H, T, test_case defined
    return (context['Q'], context['E'], context['q0'], context['F'],
            context['H'], context['T'], context['test_case'])

# Usage
file_path = r"C:\Users\hp\OneDrive\Desktop\SAFA\safa1.txt"
Q, E, q0, F, H, T, test_case = load_safa_from_pyfile(file_path)

# Now you can use your SAFA class as before
M = SAFA(Q, E, q0, F, H, T)

for i, test in enumerate(test_case):
    result = M.accepts(test)
    print(f"Test case {i+1} accepted? {result}")
