import sys
from convert import *

def main(argv):
	for line in sys.stdin:
		print('-----------------------------------------------')
		a = eval(line)
		print(a)
		# for element in a:
		# 	print element
		s = Sentence(a)
		print(s.IsAtom(), s.IsNegation(), s.IsConjunction(), s.IsDisjunction(), s.IsImplication(), s.IsBiconditional())
		cnf_s = CNFConvert(s)
		print(cnf_s)
		print('-----------------------------------------------')
		clauses = GetClauses(cnf_s)
		for clause in clauses:
			a = Clause(clause)

if __name__ == "__main__":
	#start_time = time.clock()
	main(sys.argv)