from typing import List, Tuple, Dict
from collections import deque
from copy import deepcopy
import copy
import ast

class CCA:
    def __init__(self, Q, E, I, F, T):
        self.Q = Q                  # States
        self.E = E          # Alphabet
        self.I = I                  # Initial states
        self.F = F                  # Final states
        self.T = T          # (q, a, cond, inst, q_next)

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


    # def accepts(self, input_sequence: List[Tuple[str, str]]) -> bool:
    #     initial_counter = {}  # All counters start at 0
    #     queue = deque()
    #     for start in self.I:
    #         queue.append((start, 0, initial_counter))

    #     while queue:
    #         state, pos, counter = queue.popleft()
            
    #         if pos == len(input_sequence):
    #             if state in self.F:
    #                 return True
    #             continue

    #         a, d = input_sequence[pos]

    #         for (q_curr, sym_t, cond, inst), q_next_set in self.T.items():
    #             for q_next in q_next_states:
    #                 if q != state or sym != a:
    #                     continue
                    
    #                 count = counter.get(d, 0)
    #                 if self.evaluate_condition(count, cond):
    #                     new_counter = copy.deepcopy(counter)
    #                     self.apply_instruction(count, inst, d, new_counter)
    #                     queue.append((q_next, pos + 1, new_counter))

    #     return False

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

                for (q_curr, sym_t, cond, inst), q_next_set in self.T.items():
                    if q != q_curr or sym != sym_t:
                        continue

                    if self.evaluate_condition(count, cond):
                        new_h = deepcopy(h)
                        self.apply_instruction(count, inst, data, new_h)

                        for q_next in q_next_set:
                            queue.append((q_next, i + 1, new_h))

        return False


def test():
    Q = {'q0', 'q1'}
    E = {'a', 'b'}
    I = {'q0'}
    F = {'q0'}

    # Transition format: (current_state, input_symbol, (condition_op, value), instruction, next_state)
    T = {
        ('q0', 'a', ('=', 0), '+1'): {'q0'},
        ('q0', 'a', ('=', 1), '0'): {'q1'},
        ('q0', 'b', ('>=', 0), '0'): {'q0'},
        ('q1', 'a', ('>=', 0), '0'): {'q1'},
        ('q1', 'b', ('>=', 0), '0'): {'q1'}
    }

    cca = CCA(Q, E, I, F, T)

    test_cases = [
        [('a', '1'), ('a', '2'), ('a', '3')],    
        [('a', '1'), ('a', '2'), ('a', '1')],    
        [('b', '1'), ('a', '5'), ('b', '1')],     
        [('a', '7'), ('b', '9'), ('a', '7')],   
    ]

    for i, (input_seq) in enumerate(test_cases):
        result = cca.accepts(input_seq)
        print(f"Test case {i+1}: {result}")


def parse_cca_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    # Define a safe namespace for exec
    namespace = {}
    exec(content, {}, namespace)

    Q = set(namespace['Q'])
    E = set(namespace['E'])
    I = set(namespace['I'])
    F = set(namespace['F'])
    T = dict(namespace['T'])
    test_cases = list(namespace['test_cases'])

    return Q, E, I, F, T, test_cases


file_path = r"C:\Users\hp\OneDrive\Desktop\Automata Tools\CCA\cca2.txt"
Q, E, I, F, T, test_cases = parse_cca_file(file_path)
cca = CCA(Q, E, I, F, T)
for i, (input_seq) in enumerate(test_cases):
    result = cca.accepts(input_seq)
    print(f"Test case {i+1}: {result}")

# test()
