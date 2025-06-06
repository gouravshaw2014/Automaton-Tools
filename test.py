from NFA.nfa import NFA 
from RA.ra import RA
from SAFA.safa import SAFA
from CCA.cca import CCA
from CMA.cma import CMA


nfa = NFA({'q0', 'q1', 'q2'}, {'a', 'b'}, [('q0', 'a', {'q0', 'q1'})], 'q0', {'q1'})
if nfa.accepts('b'):
    print("Accepted")
else:
    print("Rejected")