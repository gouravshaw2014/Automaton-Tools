from Automata import *


file_path_1 = r"C:\Users\hp\OneDrive\Desktop\Automata Tools\Samples\nfa_sample_1.txt"
file_path_2 = r"C:\Users\hp\OneDrive\Desktop\Automata Tools\Samples\ra_sample_1.txt"
file_path_3 = r"C:\Users\hp\OneDrive\Desktop\Automata Tools\Samples\safa_sample_1.txt"
file_path_4 = r"C:\Users\hp\OneDrive\Desktop\Automata Tools\Samples\cca_sample_1.txt"
file_path_5 = r"C:\Users\hp\OneDrive\Desktop\Automata Tools\Samples\cma_sample_1.txt"

print("\nNFA")
parse_nfa(file_path_1)

print("\nRA")
parse_ra(file_path_2)

print("\nSAFA")
parse_safa(file_path_3) 

print("\nCCA")
parse_cca(file_path_4)

print("\nCMA")
parse_cma(file_path_5)
