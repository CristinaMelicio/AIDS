import sys
from convert import *

def main(argv):
	clause_list = []
	final_clause_list = []
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
			aux = Clause(clause)
			# only add clauses that are not always True
			if aux.symbols != True:
				clause_list.append(aux)

	print('-----------------------------------------------')
	for clause in clause_list:
		print(clause)
	print('-----------------------------------------------')
	# remove clauses which contain others
	print(len(clause_list))
	for clause1 in clause_list:
		flag = True
		list_to_remove = []
		if len(final_clause_list) == 0:
			final_clause_list.append(clause1)
			flag = False
		else:
			aux = len(final_clause_list)
			for j in range(aux):
				clause2 = final_clause_list[j]
				if clause1.Contains(clause2):
					flag = False
				elif clause2.Contains(clause1):
					list_to_remove.append(j)
		
		final_clause_list = [x for i,x in enumerate(final_clause_list) if not(i in list_to_remove)]
		if flag:
			final_clause_list.append(clause1)


	print('-----------------------------------------------')		
	for clause in final_clause_list:
		print(clause)

if __name__ == "__main__":
	#start_time = time.clock()
	main(sys.argv)