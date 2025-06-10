from collections import defaultdict, deque
from typing import List, Tuple, Dict, Set
from copy import deepcopy

class NFA:
    def __init__(self, Q, E, T, q0, F):
        self.Q = Q
        self.E = E
        self.T = self.convert(T)  # Transitions: (q, a) → q'
        self.q = q0
        self.q0 = q0
        self.F = F

    def convert(self,T):
        CT = {}
        for state, symbol, next_states in T:
            key = (state, symbol)
            if key in CT:
                CT[key] |= next_states  # Union the sets
            else:
                CT[key] = set(next_states)
        return CT

    def accepts(self, string):
        current_states = {(self.q0, 0)}  # (state, position in string)
        count=0
        while current_states:
            next_states = set()
            
            for state, pos in current_states:
                if pos == len(string):
                    # Accept only if we're in the final state at end
                    if state in self.F:
                        return True
                    continue

                a = string[pos]
                if(state,a) in self.T:
                    for next_state in self.T[(state, a)]:
                        next_states.add((next_state, pos + 1))
                        count+=1
                else:
                    continue

            current_states = next_states
            # print(current_states)
        return False

    def combine(self, nfa2):
        nfa1 = self
        Q = set()
        T = []
        F = set()
        E = nfa1.E.intersection(nfa2.E)  # Only consider common alphabet

        for q1 in nfa1.Q:
            for q2 in nfa2.Q:
                combined_state = q1 + q2
                Q.add(combined_state)

                for symbol in E:
                    next1 = nfa1.T.get((q1, symbol), set())
                    next2 = nfa2.T.get((q2, symbol), set())

                    for p1 in next1:
                        for p2 in next2:
                            next_state = p1 + p2
                            next_state_set = {next_state}
                            T.append((combined_state, symbol, next_state_set))
                            # T[(combined_state, symbol, next_state)]

                if q1 in nfa1.F and q2 in nfa2.F:
                    F.add(combined_state)

        q0 = nfa1.q0 + nfa2.q0
        return NFA(Q, E, T, q0, F)
        
    def emptiness(self):
        visited = set()
        queue = deque([self.q0])

        while queue:
            current = queue.popleft()
            if current in self.F:
                return False  # Found an accepting state

            if current in visited:
                continue
            visited.add(current)

            for symbol in self.E:
                next_states = self.T.get((current, symbol), set())
                for state in next_states:
                    if state not in visited:
                        queue.append(state)

        return True

class RA:
    def __init__(self, Q, E, T, R0, U, q0, F):

        self.Q = Q
        self.E = E
        self.T = self.convert(T)  # Transitions: (q, a, i) → q'
        self.R = R0  # Current register config: [k] → D⊥
        self.U = U  # Update function: (q, a) → j
        self.q0 = q0
        self.F = F

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
        current_states = {(self.q0, 0, frozenset((h, str(v)) for h, v in self.R.items()))}
        
        while current_states:
            next_states = set()
            for state, pos, r_frozen in current_states:
                r_cur = dict(r_frozen)

                if pos == len(string):
                    if state in self.F:
                        current, peak = tracemalloc.get_traced_memory()
                        return True
                    continue

                a, d = string[pos]
                matched = False

                # Case 1: d matches existing register value
                for reg, val in r_cur.items():
                    if val == d and (state, a, reg) in self.T:
                        matched = True
                        for next_state in self.T[(state, a, reg)]:
                            next_states.add((next_state, pos + 1, r_frozen))  # No change to registers

                if matched:
                    continue

                # Case 2: fresh value
                if (state, a) in self.U:
                    j = self.U[(state, a)]
                    r_next = dict(r_cur)
                    r_next[j] = d
                    if (state, a, j) in self.T:
                        for next_state in self.T[(state, a, j)]:
                            next_states.add((next_state, pos + 1, frozenset(r_next.items())))
                            
            current_states = next_states
        return False

class CCA:
    def __init__(self, Q, E, I, F, T):
        self.Q = Q                  # States
        self.E = E          # Alphabet
        self.I = I                  # Initial states
        self.F = F                  # Final states
        self.T = self.convert(T)          # (q, a, cond, inst, q_next)

    def convert(self,T):
        '''
        Convert to CCA_T format for optimaized selction of next states
            {('q0', 'a'): ((('=', 0), '+1', {'q1', 'q0'}), (('=', 1), '0', {'q1'})),
            ('q0', 'b'): ((('>=', 0), '0', {'q0'}), (('>=', 0), '0', {'q1'})),
            ('q1', 'a'): ((('>=', 0), '0', {'q1'}),),
            ('q1', 'b'): ((('>=', 0), '0', {'q1'}),)}

        '''
        temp = defaultdict(set)

        # Merge transitions with same (state, symbol, condition, instruction)
        for state, symbol, condition, instruction, next_states in T:
            key = (state, symbol, condition, instruction)
            temp[key].update(next_states)

        # Convert to final CCA_T format
        grouped = defaultdict(list)
        for (state, symbol, condition, instruction), next_states in temp.items():
            grouped[(state, symbol)].append((condition, instruction, next_states))

        # Convert lists to tuples for consistency
        for key in grouped:
            grouped[key] = tuple(grouped[key])

        return dict(grouped)

    def evaluate_condition(self, count: int, cond: Tuple[str, int]) -> bool:
        op, val = cond
        if op == '=':
            return count == val
        elif op == '>=':
            return count >= val
        elif op == '>':
            return count > val
        elif op == '<':
            return count < val
        elif op == '<=':
            return count <= val
        elif op == '!=':
            return count != val
        else:
            raise ValueError(f"Unknown condition: {cond}")

    def apply_instruction(self, count: int, inst: str, data: str, counter: Dict[str, int]) -> None:
        if inst == '*':
            if data in counter:
                counter[data] = 0  # Reset completely
        elif inst == '0':
            pass  # Keep the count as is (no update needed)
        elif inst.startswith('+'):
            counter[data] = count + int(inst[1:])
        else:
            raise ValueError(f"Invalid instruction: {inst}")

    def accepts(self, input_seq):
        queue = deque()

        # Initialize the queue with all initial states and an empty counter dictionary
        for state in self.I:
            queue.append((state, 0, {}))  # (current_state, input_index, counter_dict)

        while queue:
            q, i, h = queue.popleft()

            if i == len(input_seq):
                if q in self.F:
                    return True
                continue

            sym, data = input_seq[i]
            count = h.get(data, 0)

            key = (q, sym)
            if key in self.T:
                for cond, inst, q_next_set in self.T[key]:
                    if self.evaluate_condition(count, cond):
                        new_h = deepcopy(h)
                        self.apply_instruction(count, inst, data, new_h)
                        for q_next in q_next_set:
                            queue.append((q_next, i + 1, new_h))

        return False

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

def parse_nfa(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    namespace = {}
    exec(content, {}, namespace)  # Safe limited scope

    Q = set(namespace['Q'])
    E = set(namespace['E'])
    F = set(namespace['F'])
    T = list(namespace['T'])
    q0 = namespace['q0']
    test_cases = list(namespace['test_cases'])

    nfa = NFA(Q, E, T, q0, F)
    result = 'Emptiness' if nfa.emptiness() else 'Not Emptiness'
    print(result)

    for i, test in enumerate(test_cases):
        result =  'Accepted' if nfa.accepts(test) else 'Rejected'
        print(f"Test case {i+1} : {result}")

def parse_ra(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    namespace = {}
    exec(content, {}, namespace)

    Q = set(namespace['Q'])
    E = set(namespace['E'])
    R0 = dict(namespace['R0'])
    T = list(namespace['T'])
    U = dict(namespace['U'])
    q0 = namespace['q0']
    F = set(namespace['F'])
    test_cases = namespace['test_cases']

    ra = RA(Q, E, T, R0, U, q0, F)
    # result = 'Emptiness' if ra.emptiness() else 'Not Emptiness'
    # print(result)

    for i, test in enumerate(test_cases):
        result =  'Accepted' if ra.accepts(test) else 'Rejected'
        print(f"Test case {i+1} : {result}")

def parse_safa(filepath):
    with open(file_path, 'r') as f:
        content = f.read()

    namespace = {}
    exec(content, {}, namespace)

    Q = set(namespace['Q'])
    E = set(namespace['E'])
    q0 = namespace['q0']
    H = set(namespace['H'])
    F = set(namespace['F'])
    T = list(namespace['T'])    
    test_cases = list(namespace['test_cases'])

    safa = SAFA(Q, E, q0, F, H, T)
    result = 'Emptiness' if safa.emptiness() else 'Not Emptiness'
    print(result)

    for i, test in enumerate(test_cases):
        result =  'Accepted' if safa.accepts(test) else 'Rejected'
        print(f"Test case {i+1} : {result}")

def parse_cca(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    namespace = {}
    exec(content, {}, namespace)

    Q = set(namespace['Q'])
    E = set(namespace['E'])
    I = set(namespace['I'])
    F = set(namespace['F'])
    T = list(namespace['T'])    
    test_cases = list(namespace['test_cases'])

    cca = CCA(Q, E, I, F, T)

    for i, test in enumerate(test_cases):
        result =  'Accepted' if cca.accepts(test) else 'Rejected'
        print(f"Test case {i+1} : {result}")

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

    cma = CMA(Q, E, T, q0, Fl, Fg)

    for i, test in enumerate(test_cases):
        result =  'Accepted' if cma.accepts(test) else 'Rejected'
        print(f"Test case {i+1} : {result}")