import sys
from biblio import *

def main(argv):
	clause_list = []
	for line in sys.stdin:
		a = eval(line)
		# print('-----------------------------------------------')
		# print('-- Sentence to convert')
		# print(a)
		s = Sentence(a)
		#print(s.IsAtom(), s.IsNegation(), s.IsConjunction(), s.IsDisjunction(), s.IsImplication(), s.IsBiconditional())
		cnf_s = CNFConvert(s)
		# print('-----------------------------------------------')
		# print('-- CNF Conversion Result')
		# print(cnf_s)
		clauses = OutputConvert(cnf_s)

		# print('-----------------------------------------------')
		# print('-- Resultant Clauses')
		for clause in clauses:
			# only add clauses that are not always True
			print(clause)

if __name__ == "__main__":
	#start_time = time.clock()
	main(sys.argv)