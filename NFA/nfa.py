from collections import defaultdict, deque
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
        queue = deque()
        queue.append((self.q0, 0))
        
        while queue:
            state, pos = queue.popleft()
            if pos == len(string):
                # Accept only if we're in the final state at end
                if state in self.F:
                    return True
                continue

            a = string[pos]
            if(state,a) in self.T:
                for next_state in self.T[(state, a)]:
                    queue.append((next_state, pos + 1))
                    
            else:
                continue

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
        