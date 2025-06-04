from collections import defaultdict, deque
class NFA:
    # def __init__(self, n):
    #     self.n = n
    #     self.states = list(range(n + 1))  # q0 to qn
    #     self.start_state = 0
    #     self.final_state = n
    #     self.alphabet = {'0', '1'}
    #     self.transitions = self._build_transitions()
    def __init__(self, Q, E, T, q0, F):
        self.Q = Q
        self.E = E
        self.T = convert(T)  # Transitions: (q, a) → q'
        self.q = q0
        self.q0 = q0
        self.F = F
    # def _build_transitions(self):
    #     T = defaultdict(lambda: defaultdict(set))

    #     # q0: loop on any symbol or guess '1' is the n-th last bit → go to q1
    #     for sym in self.alphabet:
    #         T[0][sym].add(0)
    #     T[0]['1'].add(1)  # Guessing current '1' is n-th last bit

    #     # q1 to q(n-1): move forward on any input
    #     for i in range(1, self.n):
    #         for sym in self.alphabet:
    #             T[i][sym].add(i + 1)
    #     # print(T)
    #     return T

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


def convert(T):
    CT = {}
    for state, symbol, next_states in T:
        key = (state, symbol)
        if key in CT:
            CT[key] |= next_states  # Union the sets
        else:
            CT[key] = set(next_states)
    return CT


def a():
    Q = {'q0','q1','q2'}
    E = {'a','b'}
    F = {'q2'}
    T = {
        ('q0','a', {'q0','q1'}),
        ('q0','b', {'q0'}),       
        ('q1','a', {'q2'}), 
        ('q2','a', {'q2'}),   
        ('q2','b', {'q2'})
    } 
    q0='q0'
    nfa = NFA(Q, E, T, q0, F)
    print(nfa.accepts('abbbbbbbbbaa'))

def parse_automaton_txt(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    namespace = {}
    exec(content, {}, namespace)  # Safe limited scope

    Q = set(namespace['Q'])
    E = set(namespace['E'])
    F = set(namespace['F'])
    T = list(namespace['T'])
    q0 = namespace['q0']
    test_case = list(namespace['test_case'])

    return Q, E, F, T, q0, test_case

# Path to your file
file_path = r"C:\Users\hp\OneDrive\Desktop\Automata Tools\NFA\nfa2.txt"

# Parse the file
Q, E, F, T, q0, test_case = parse_automaton_txt(file_path)
nfa = NFA(Q, E, T, q0, F)
result = nfa.emptiness()
print("Emptiness =" ,result )
for i in test_case:
    print(nfa.accepts(i))