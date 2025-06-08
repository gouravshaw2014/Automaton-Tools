from typing import List, Tuple, Dict, Set
from collections import deque, defaultdict
from copy import deepcopy
from NFA.nfa import NFA

class SAFA:
    def __init__(self, Q, E, q0, F, H, T):
        self.Q = Q
        self.E = E
        self.q0 = q0
        self.F = F
        self.H = H
        self.T = self.convert(T)  # { (state, symbol, condition) : set of "next_state,set_name" }

    def convert(self,T):
        grouped = defaultdict(set)

        for state, symbol, condition, next_states in T:
            key = (state, symbol, condition)
            grouped[key].update(next_states)

        St = defaultdict(list)
        for (state, symbol, condition), targets in grouped.items():
            St[(state, symbol)].append((condition, targets))

        # Optional: convert lists to tuples for consistent format
        for key in St:
            St[key] = tuple(St[key])

        return dict(St)

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
        H_cur = deepcopy(self.H)
        initial_config = (self.q0, H_cur)
        queue = deque()
        queue.append((0, initial_config))
        
        while queue:
            pos, (q, H_copy) = queue.popleft()
            if pos == len(w):
                if q in self.F:
                    return True
                continue

            symbol, data = w[pos]
            key = (q, symbol)

            if key in self.T:
                for cond, ns_action_set in self.T[key]:
                    if not self.condition_check(cond, data, H_copy):
                        continue
                    for ns_action in ns_action_set:
                        if ',' in ns_action:
                            q_next, set_name = ns_action.split(',')
                            
                        else:
                            q_next, set_name = ns_action, '-'  # default to no set

                        H_next = deepcopy(H_copy)
                        if set_name != '-':
                            H_next[set_name].add(data)

                        queue.append((pos + 1, (q_next, H_next)))

        return False

    def convert_nfa_T(self):
        NFA_T = []
        E = set()
        for (q, a), cond_targets in self.T.items():
            for cond, target_set in cond_targets:
                hi, val = cond.split(',')  # e.g., 'h2', '1'
                for target in target_set:
                    q_next, h_next = target.split(',')
                    if h_next != '-':
                        ext_symbol = f"{a},{hi},{val},{h_next}"
                    else:
                        ext_symbol = f"{a},{hi},{val},-"

                    NFA_T.append((q, ext_symbol, {q_next}))

        H = self.H.keys()

        for a in self.E:
            for h1 in H:
                for val in {'0', '1'}:
                    ext_symbol = f"{a},{h1},{val},-"
                    E.add(ext_symbol)
                    for h2 in H:
                        ext_symbol = f"{a},{h1},{val},{h2}"
                        E.add(ext_symbol)
        return E, NFA_T

    def convert_safa_T(self, E):
        h = len(self.H.keys())
        Q = set()
        for i in range(2 ** h):
            binary = format(i, f'0{h}b')  # Pad binary to length n
            Q.add(f'q{binary}')
        F = deepcopy(Q)
        q0 = f'q{'0'*h}'
        T = []
        for q_curr in Q:
            for a in E:
                for q_next in Q:
                    if self.differnce(q_curr, q_next):
                        continue
                    
                    symbol, hi, val, h_next = a.split(',')

                    index = int(hi[1])
                    if val == '0'and q_curr[-index] == '0':
                        continue
                    if h_next != '-':
                        index = int(h_next[1])
                        if q_next[-index] == '0':
                            continue
                    T.append((q_curr, a, {q_next}))
                    

        return Q, T, q0, F

    def differnce(self, q_curr, q_next):
        if int(q_curr[1:]) > int(q_next[1:]):
            return True
        count = 0
        i = 1
        while(i < len(q_curr)):
            if count == 2:
                return True
            if q_curr[i] == '0' and q_curr[i] != q_next[i]:
                count += 1
            i += 1
        if count == 2:
                return True
        return False
        

    def emptiness(self):
        E, T1 = self.convert_nfa_T()
        # print(T1)
        nfa1 = NFA(self.Q, E, T1, self.q0, self.F)
        Q2, T2, q02, F2 = self.convert_safa_T(E)
        # print(T2)
        nfa2 = NFA(Q2, E, T2, q02, F2)
        nfa = nfa1.combine(nfa2)
        # print(nfa.T)
        return nfa.emptiness()    



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
    T = [
        ('q0', 'a', 'h1,1', {'q0,h1','q1,h2'}),
        ('q0', 'a', 'h2,1', {'q3,h1','q1,h2'}),
        ('q0', 'a', 'h1,0', {'q0,h1'}), 
        ('q1', 'a', 'h2,1', {'q0,-'}),
        ('q1', 'a', 'h2,0', {'q2,-'}),
        ('q2', 'a', 'h2,1', {'q2,-'}),
        ('q2', 'a', 'h2,0', {'q3,-'}),
        ('q3', 'a', 'h1,0', {'q3,-'}),
        ('q3', 'a', 'h1,1', {'q3,-'}),
    ]

    M = SAFA(Q, E, q0, F, H, T)

    w = [('a', '1'), ('a', '1'), ('a', '3'), ('a', '3'), ('a', '3')]
    print("Accepted?", M.accepts(w))  # Should process new/known with respect to h1

def parse_safa(filepath):
    with open(file_path, 'r') as f:
        content = f.read()

    namespace = {}
    exec(content, {}, namespace)

    Q = set(namespace['Q'])
    E = set(namespace['E'])
    q0 = namespace['q0']
    H = dict(namespace['H'])
    F = set(namespace['F'])
    T = list(namespace['T'])    
    test_cases = list(namespace['test_cases'])

    return Q, E, q0, F, H, T, test_cases
    # context = {}
    # with open(filepath, 'r') as f:
    #     code = f.read()
    # exec(code, {}, context)
    # # Now context dict has Q, E, q0, F, H, T, test_case defined
    # return (context['Q'], context['E'], context['q0'], context['F'],
    #         context['H'], context['T'], context['test_case'])

# Usage
file_path = r"C:\Users\hp\OneDrive\Desktop\Automata Tools\SAFA\safa3.txt"
Q, E, q0, F, H, T, test_case = parse_safa(file_path)

# Now you can use your SAFA class as before
M = SAFA(Q, E, q0, F, H, T)
if M.emptiness():
    print("Emptiness")
else:
    print("Not Emptiness")
# print(M.T)
# if ('q0', 'a') in M.T:
#     print("TRUE")

for i, test in enumerate(test_case):
    result = M.accepts(test)
    print(f"Test case {i+1} accepted? {result}")
# a()