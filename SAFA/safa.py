from typing import List, Tuple, Dict, Set
from collections import deque, defaultdict
from copy import deepcopy

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