# Automaton Tools
### I want to create Toolbox of automata mainly NFA(Non-Deterministic Finite Automata), RA(Register Automata), SAFA(Set Augmented Finite Automata), CCA(Class Count Automata) and CMA(Class Memory Automata).

-------------------------------------------------

## About
For the time being, I have created class structure of individual types of automatas. Each class has its constructors to initialize there corresponding machines tuples. The class has "accepts" method which takes string / sequence of (symbol,data value) as argument and return boolean value to indicate whether the input is accepted or rejected.

-------------------------------------------------

## NFA(Non-Deterministic Finite Automata)

An NFA, or Non-Deterministic Finite Automaton, is represented by a 5-tuple, which includes the following components:

Q: A finite set of states.

Σ/E: A finite set of input symbols.

δ/T: The transition function, which maps a state and an input symbol to a subset of states. For an NFA, this is typically expressed as δ:Q×Σ→P(Q), where P(Q) denotes the power set of Q.

q₀: The initial state, which is an element of Q.

F: A set of final or accepting states, which is a subset of Q.

To create an NFA object initialize in the order NFA(Q, E, T, q0, F) or can give the text file path to parse and test it with the test cases.

-------------------------------------------------

### Representation of (Q, E, T, q0, F, test_case) in text file
#### Note :
Q, E, T, q0, F and test_case should be mentioned once in the text file and the elements must be in single quotes and maintain the Brackets associates with it.

### Example 
--States 

Q = {'q0','q1','q2'}

--Alphabet

E = {'a','b'}

--Transitions: ('current_state', 'input_symbol' , {'next_state'})

T = [

    ('q0','a', {'q0','q1'}),

    ('q0','b', {'q0'}),

    ('q1','a', {'q2'}),

    ('q2','a', {'q2'}),

    ('q2','b', {'q2'})

]

--Initial state

q0 = 'q0'

--Accepting state

F = {'q2'}

--Test cases as array of strings

test_case = [

    'abbabaabbabab',

    'babbabaabbaba',

    'abababaaabbbabab'

]

-------------------------------------------------

To recognize the intersection of two different NFA languages, you can use the combine method which can be invoked using an nfa taking another nfa as argument. This involves creating a new NFA where the states are pairs of states from the original NFAs. Each state in the new NFA corresponds to a combination of states from both original NFAs.

To check for emptiness of the NFA, you can use the emptiness metthod which returns boolean value "True" if the NFA doesn't accepts any strings at all, otherwise "False".

-------------------------------------------------

## RA(Register Automata)
An RA, or Register Automata, is represented by a 6-tuple, which includes the following components:

Q: A finite set of states.

Σ/E: A finite set of input symbols.

δ/T: The transition relation is δ ⊆ (Q × Σ × [k] × Q). We assume that for all i, j ∈ [k] if i 6= j and τ0(i), τ0(j) ∈ D then τ0(i) != τ0(j) (that is, registers initially contain distinct data values).

τ0/R0: The initial register configuration given by τ0 : [k] → D⊥

U: The partial update function: (Q × Σ) → [k].

q₀: The initial state, which is an element of Q.

F: A set of final or accepting states, which is a subset of Q.

To create an RA object initialize in the order RA(Q, E, T, R0, U, q0, F) or can give the text file path to parse and test it with the test cases.

-------------------------------------------------

### Representation of (Q, E, T, R0, U, q0, F, test_case) in text file
#### Note :
Q, E, T, R0, U, q0, F and test_case should be mentioned once in the text file and the elements must be in single quotes and maintain the Brackets associates with it.

### Example 
--States

Q = {'q0', 'q1', 'q2'}

--Alphabet

E = {'a'}

--Initial register contents: {'register index' : 'data value'} for uninitialized (⊥) = None(without quotes)

R0 = {'1': None, '2': None}

--Transitions: ('current_state' , 'input_symbol' , 'register_index' , {'next_state'})

T = [

    ('q0', 'a', '1', {'q1'}),

    ('q1', 'a', '1', {'q0'}),

    ('q1', 'a', '2', {'q2'})

]

--Update function: ('state', 'input_symbol') : 'register_index' to update with fresh data

U = {

    ('q0', 'a'): '1',

    ('q1', 'a'): '2'

}

--Initial state

q0 = 'q0'

--Accepting state

F = {'q0'}

--Test cases as sequence of (input_symbol, data_value)

test_case = [

    [('a', '0'),('a', '0'),('a', '1'),('a', '1')],

    [('a', '0'), ('a', '0'), ('a', '0'),('a','0')],

    [('a', '5'), ('a', '8'), ('a', '7')]

]

-------------------------------------------------

## SAFA(Set Augmented Finite Automata)
An SAFA, or Set Augmented Finite Automata, is represented by a 6-tuple, which includes the following components:

Q: A finite set of states.

Σ/E: A finite set of input symbols.

q₀: The initial state, which is an element of Q.

F: A set of final or accepting states, which is a subset of Q.

H: The finite set of finite sets of data values.

δ/T: The transition relation is δ ⊆ Q×Σ×C×OP×Q where C = {p(hi), !p(hi) | hi ∈H}, hi denotes the ith set in H, and OP = {−, ins(hi) | hi ∈ H}.

To create an SAFA object initialize in the order SAFA(Q, E, q0, F, H, T) or can give the text file path to parse and test it with the test cases.

-------------------------------------------------

### Representation of (Q, E, q0, F, H, T, test_cases) in text file
#### Note :
Q, E, q0, F, H, T and test_cases should be mentioned once in the text file and the elements must be in single quotes and maintain the Brackets associates with it.

### Example 
--States

Q = {'q0', 'q1','q2', 'q3'}

--Alphabet

E = {'a'}

--Initial state

q0 = 'q0'

--Accepting state(s)

F = {'q1', 'q3'}

--Set of sets: {'set number'}

H = {'h1', 'h2'}

--Transition function: ('state', 'symbol', 'set_number_to_check_its_presence,0/1', {'next_states,set_number_for_insertion'})

"0" for known / "1" for new and '-' for no insertion

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

--Array of test case with sequence (symbol, data value)

test_cases=[

    [('a', '1'), ('a', '2'), ('a', '4'), ('a', '3'), ('a', '3'),('a','4')],

    [('a', '1'), ('a', '2'), ('a', '3'), ('a', '3'), ('a', '1'),('a', '2'), ('a', '2')]
    
]

-------------------------------------------------

To check for emptiness of the SAFA, you can use the emptiness metthod which returns boolean value "True" if the SAFA doesn't accepts any strings at all, otherwise "False".

-------------------------------------------------

## CCA(Class Count Automata)
An CCA, or Class Count Automata, is represented by a 5-tuple, which includes the following components:

Q: A finite set of states.

Σ/E: A finite set of input symbols.

I: The set of initial states, which is an element of Q.

F: A set of final or accepting states, which is a subset of Q.

δ/T: The transition relation is given by: δ ⊆ (Q x Σ x C x I x U x Q), where C is a finite subset of C and U is a finite subset of N.

To create an CCA object initialize in the order CCA(Q, E, I, F, T) or can give the text file path to parse and test it with the test cases.

-------------------------------------------------

### Representation of (Q, E, I, F, T, test_cases) in text file
#### Note :
Q, E, I, F, T and test_cases should be mentioned once in the text file and the elements must be in single quotes and maintain the Brackets associates with it.

### Example 
--States

Q = {'q0', 'q1'}

--Alphabet

E = {'a', 'b'}

--Set of Initial States

I = {'q0'}

--Set of Final States

F = {'q1'}

--Transition format: ('current_state', 'input_symbol', ('condition_op', 'value'), 'instruction', {'next_state'})

--Instruction format => '*' : reset, '0' : no change , '+n' : add n

T = [

    ('q0', 'a', ('<', 2), '+1',{'q0'}),

    ('q0', 'a', ('=', 2), '0', {'q1'}),

    ('q0', 'b', ('>=', 0), '0', {'q0'}),

    ('q1', 'a', ('=', 2), '0', {'q1'}),

    ('q1', 'a', ('<', 2), '+1', {'q0'}),

    ('q1', 'b', ('>=', 0), '0', {'q1'})

]

--Test cases as sequence of (input_symbol, data_value)

test_cases = [

    [('a', '1'), ('a', '2'), ('a', '3'), ('a', '2'), ('a', '3'), ('a', '2'), ('a', '3')],   

    [('a', '1'), ('a', '2'), ('a', '1')],   

    [('b', '1'), ('a', '5'), ('b', '1'), ('a', '5'), ('a', '5')],   

    [('a', '7'), ('b', '9'), ('a', '7')],   

]

-------------------------------------------------

## CMA(Class Memory Automata)
An CCA, or Class Count Automata, is represented by a 5-tuple, which includes the following components:

Q: A finite set of states.

Σ/E: A finite set of input symbols.

I: The set of initial states, which is an element of Q.

F: A set of final or accepting states, which is a subset of Q.

δ/T: The transition relation is given by: δ ⊆ (Q x Σ x C x I x U x Q), where C is a finite subset of C and U is a finite subset of N.

To create an CMA object initialize in the order CMA(Q, E, T, q0, Fl, Fg) or can give the text file path to parse and test it with the test cases.

-------------------------------------------------

### Representation of (Q, E, T, q0, Fl, Fg, test_cases) in text file
#### Note :
Q, E, T, q0, Fl, Fg and test_cases should be mentioned once in the text file and the elements must be in single quotes and maintain the Brackets associates with it.

### Example 
--States

Q = {'q0', 'qa', 'qb'}

--Alphabet

E = {'a', 'b'}

--Transition format: ('current_state', 'input_symbol', 'last_state', {'next_state'})

-- last_state will be '-' for no last_state i.e. new data value

T = [

    ('q0', 'a', '-', {'qa'}),
    
    ('qa', 'a', '-', {'qa'}),
    
    ('qb', 'a', '-', {'qa'})

]

--Initial state

q0 = 'q0'

--Set of Local Final States

Fl = {'q0', 'qa', 'qb'}

--Set of Global Final States

Fg = {'q0', 'qa', 'qb'}

--Test cases as sequence of (input_symbol, data_value)

test_cases = [

    [('a', '1'), ('a', '2'), ('a', '3'), ('a', '2'), ('a', '3'), ('a', '2'), ('a', '3')],   

    [('a', '1'), ('a', '2'), ('a', '1')],   

    [('b', '1'), ('a', '5'), ('b', '1'), ('a', '5'), ('a', '5')],   

    [('a', '7'), ('b', '9'), ('a', '7')],   

]

-------------------------------------------------