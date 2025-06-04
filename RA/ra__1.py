from typing import List, Tuple, Dict
from collections import deque
import tracemalloc
import random
import ast
import re

class RegisterAutomaton:
    def __init__(self, Q, E, T, R0, U, q0, F, k):

        self.Q = Q
        self.E = E
        self.T = T  # Transitions: (q, a, i) → q'
        self.R = R0  # Current register config: [k] → D⊥
        self.U = U  # Update function: (q, a) → j
        self.q0 = q0
        self.F = F
        self.k = k


    def accepts(self, string: List[Tuple[str, str]]) -> bool:

        # Initial configuration: (state, register values as tuple, input index)
        R=self.R
        current_states = {(self.q0, 0)}
        # print(current_states)
        while current_states:
            next_states = set()            
            for state, pos in current_states:
                if pos == len(string):
                    if state in self.F:
                        current, peak = tracemalloc.get_traced_memory()
                        return True
                    continue

                a, d = string[pos]
                
                matched = False

                # Case 1: d matches register content and a transition exists
                for r,i in R.items():
                    if i == d and (state, a, r) in self.T:
                        matched = True
                        if(state,a,r) in self.T:
                            for next_state in self.T[(state, a, r)]:
                                next_states.add((next_state, pos + 1))
                        
                if matched:
                    continue
                # Case 2: d is fresh and update rule exists
                if not matched and (state, a) in self.U:
                    j = self.U[(state, a)]
                    self.R[j] = d
                    if(state,a,j) in self.T:
                        for next_state in self.T[(state, a, j)]:
                            next_states.add((next_state, pos + 1))
                    else:
                        continue
            current_states = next_states
        return False

def generate_input_sequence(alphabet: set[str], size: int, num_digits: int = 20 ) -> List[Tuple[str, str]]:

    return [
        (random.choice(list(alphabet)), str(random.randint(0, 10**num_digits - 1)))
        for _ in range(size)
    ]

def a():
    # States
    Q = {'q0', 'q1', 'q2'}

    # Alphabet
    E = {'a', 'b'}

    # Number of registers
    k = 2

    # Initial register contents (uninitialized = None)
    R0 = {0: None, 1: None}

    # Transitions: (current_state, input_symbol, register_index) -> next_state
    T = {
        ('q0', 'a', '0'): {'q0','q1'},
        ('q0', 'b', '0'): {'q0'},       
        ('q1', 'a', '1'): {'q1'},
        ('q1', 'b', '1'): {'q1'},
        ('q1', 'a', '0'): {'q2'}, 
        ('q2', 'a', '0'): {'q2'},   
        ('q2', 'b', '0'): {'q2'},
        ('q2', 'a', '1'): {'q2'},   
        ('q2', 'b', '1'): {'q2'}   
        # Add self loops if necessary, or no transition means rejection
    }

    # Update function: (state, input_symbol) -> register_index to update with fresh data
    U = {
        ('q0', 'a'): '0',
        ('q0','b'): '0',  # On first 'a' in q0, store data in r0
        ('q1', 'a'): '1',
        ('q1', 'b'): '1',
        ('q2', 'a'): '1',
        ('q2', 'b'): '1'   # On 'b' in q1, store new data in r1
    }

    # Initial state
    q0 = 'q0'

    # Accepting state(s)
    F = {'q2'}

    RA = RegisterAutomaton(Q, E, T, R0, U, q0, F, k)

    # Test inputs
    input_sequence = [('a', '0'),('b', '1'), ('a', '0'), ('b', '1'), ('a', '0')]  # Should accept
    # input_sequence = generate_input_sequence(E, 100)
    tracemalloc.start()
    print(RA.accepts(input_sequence))  # True
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"Memory Used: {current / 1024:.2f} KB (Peak: {peak / 1024:.2f} KB)")

def parse_register_automaton(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    namespace = {}
    exec(content, {}, namespace)

    Q = set(namespace['Q'])
    E = set(namespace['E'])
    k = int(namespace['k'])
    R0 = dict(namespace['R0'])
    T = {k: set(v) for k, v in namespace['T'].items()}
    U = dict(namespace['U'])
    q0 = namespace['q0']
    F = set(namespace['F'])
    test_case = namespace['test_case']

    return Q, E, k, R0, T, U, q0, F, test_case



file_path = r"C:\Users\hp\OneDrive\Desktop\Automata Tools\RA\ra1.txt"
Q, E, k, R0, T, U, q0, F, test_case = parse_register_automaton(file_path)
R_initial = dict(R0)
RA = RegisterAutomaton(Q, E, T, R0, U, q0, F, k)
for i in test_case:
    print(RA.accepts(i))
    RA.R=dict(R_initial)
# a()
# print(RA)