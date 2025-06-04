from typing import List, Tuple, Dict, Set
from collections import deque

class SAFA:
    def __init__(self, Q, E, q0, F, H, T):
        self.Q = Q
        self.E = E
        self.q0 = q0
        self.F = F
        self.H = H
        self.T = T  # { (state, symbol, condition) : set of "next_state,set_name" }

    def condition_check(self, cond: str, data: str, H_copy: Dict[str, Set[str]]) -> bool:
        if cond == '-' or cond == '':
            return True

        parts = cond.split(',')
        if len(parts) != 2:
            raise ValueError(f"Invalid condition format: {cond}")

        set_name, flag = parts
        if set_name == '-':
            return True

        known = data in H_copy.get(set_name, set())

        if flag == '0' and known:
            return True
        if flag == '1' and not known:
            return True

        return False

    def accepts(self, w):
        initial_config = (self.q0, {h: set(v) for h, v in self.H.items()})
        from collections import deque
        queue = deque()
        queue.append((0, initial_config))

        while queue:
            pos, (state, H_copy) = queue.popleft()

            if pos == len(w):
                if state in self.F:
                    return True
                continue

            symbol, data = w[pos]

            for (q, a, cond), next_state_actions in self.T.items():
                if q != state or a != symbol:
                    continue

                if not self.condition_check(cond, data, H_copy):
                    continue

                for ns_action in next_state_actions:
                    if ',' in ns_action:
                        q_next, set_name = ns_action.split(',')
                    else:
                        q_next, set_name = ns_action, '-'  # default to no set

                    H_next = {h: set(s) for h, s in H_copy.items()}
                    if cond.endswith(',1') and set_name != '-':
                        H_next[set_name].add(data)

                    queue.append((pos + 1, (q_next, H_next)))

        return False



def a():
    Q = {'q0', 'q1','q2', 'q3'}

    # Alphabet
    E = {'a'}

    # Initial state
    q0 = 'q0'

    # Accepting state(s)
    F = {'q1', 'q3'}

    # Set of sets
    H = {'h1': set(), 'h2': set()}

    # Transition function: (state, symbol, "0" for known / "1" for new, set_name) -> next_states (set of next_states)
    T = {
        ('q0', 'a', 'h1,1'): {'q0,h1','q1,h2'},
        ('q0', 'a', 'h2,1'): {'q3,h1','q1,h2'},
        ('q0', 'a', 'h1,0'): {'q0,h1'}, 
        ('q1', 'a', 'h2,1'): {'q0,-'},
        ('q1', 'a', 'h2,0'): {'q2,-'},
        ('q2', 'a', 'h2,1'): {'q2,-'},
        ('q2', 'a', 'h2,0'): {'q3,-'},
        ('q3', 'a', 'h1,0'): {'q3,-'},
        ('q3', 'a', 'h1,1'): {'q3,-'},
    }

    M = SAFA(Q, E, q0, F, H, T)

    w = [('a', '1'), ('a', '1'), ('a', '3'), ('a', '3'), ('a', '3')]
    print("Accepted?", M.accepts(w))  # Should process new/known with respect to h1

def load_safa_from_pyfile(filepath):
    context = {}
    with open(filepath, 'r') as f:
        code = f.read()
    exec(code, {}, context)
    # Now context dict has Q, E, q0, F, H, T, test_case defined
    return (context['Q'], context['E'], context['q0'], context['F'],
            context['H'], context['T'], context['test_case'])

# Usage
file_path = r"C:\Users\hp\OneDrive\Desktop\Automata Tools\SAFA\safa2.txt"
Q, E, q0, F, H, T, test_case = load_safa_from_pyfile(file_path)

# Now you can use your SAFA class as before
M = SAFA(Q, E, q0, F, H, T)

for i, test in enumerate(test_case):
    result = M.accepts(test)
    print(f"Test case {i+1} accepted? {result}")
# a()