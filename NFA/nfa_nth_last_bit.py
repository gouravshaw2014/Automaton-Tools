import tracemalloc
import random
from collections import defaultdict

class NFA_NthLastBit:
    def __init__(self, n):
        self.n = n
        self.states = list(range(n + 1))  # q0 to qn
        self.start_state = 0
        self.final_state = n
        self.alphabet = {'0', '1'}
        self.transitions = self._build_transitions()

    def _build_transitions(self):
        T = defaultdict(lambda: defaultdict(set))

        # q0: loop on any symbol or guess '1' is the n-th last bit → go to q1
        for sym in self.alphabet:
            T[0][sym].add(0)
        T[0]['1'].add(1)  # Guessing current '1' is n-th last bit

        # q1 to q(n-1): move forward on any input
        for i in range(1, self.n):
            for sym in self.alphabet:
                T[i][sym].add(i + 1)
        # print(T)
        return T

    def accepts(self, string):
        current_states = {(self.start_state, 0)}  # (state, position in string)
        count=0
        while current_states:
            next_states = set()
            
            for state, pos in current_states:
                if pos == len(string):
                    # Accept only if we're in the final state at end
                    if state == self.final_state:
                        print(n,count,end=" ")
                        return True
                    continue

                symbol = string[pos]
                for next_state in self.transitions[state][symbol]:
                    next_states.add((next_state, pos + 1))
                    count+=1

            current_states = next_states
        print(n,count,end=" ")
        return False

def generate_binary_strings(n):
    result = []
    
    # String with all 1s
    result.append('1' * n)
    
    # String with all 0s
    result.append('0' * n)
    
    # Generate 3 random binary strings
    for _ in range(3):
        random_string = ''.join(random.choice('01') for _ in range(n))
        result.append(random_string)
    
    return result

n_values = [2,4,8,16,32,64,128]
# test_strings = [
#     "1101010011111111111111000010000011110000000000010101111111100000001111111111111111110000000011000000111111111111100000110000110011111",
#     "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
# ]
test_strings = generate_binary_strings(15000)
# for n in n_values:
#     print(f"\nNFA Check for n = {n} (n-th last bit is '1'):")
#     nfa = NFA_NthLastBit(n)
#     for s in test_strings:
#         result = "ACCEPTED" if nfa.accepts(s) else "REJECTED"
#         print(f"{s:>10} -> {result} -> {len(s)}")
for n in n_values:
    print(f"\nNFA Check for n = {n} (n-th last bit is '1'):")
    nfa = NFA_NthLastBit(n)
    for s in test_strings:
            tracemalloc.start()

            result = "ACCEPTED" if nfa.accepts(s) else "REJECTED"

            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            print(result)
            # print(f"{s:>10} -> {result:<9} | Memory Used: {current / 1024:.2f} KB (Peak: {peak / 1024:.2f} KB)")