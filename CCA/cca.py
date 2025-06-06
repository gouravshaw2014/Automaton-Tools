from typing import List, Tuple, Dict
from collections import deque, defaultdict
from collections import defaultdict
from copy import deepcopy

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
    