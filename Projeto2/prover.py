import sys
from biblio import *
from itertools import combinations

def Simplify(KB):

	KB_len = len(KB)
	KB_new = list(KB)
	removed_flag = True
	remove_clauses = [False for i in range(KB_len)]
	checked_clauses = [False for i in range(KB_len)]
	complentary_found = False

	# do while a clause has been removed
	while removed_flag:
		removed_flag = False
		# loop on all clauses
		for i in range(KB_len):
			# only do thing if current clause is not to be removed
			if not(remove_clauses[i]):
				checked_clauses[i] = True
				# loop in all literals of clause
				for literal in KB_new[i].literals:
					# loop in all other clauses that have not yet been marked to removed
					for j in range(KB_len):
						if i!=j and not(remove_clauses[j]):
							# if clause with complementary found, stop checking
							if KB_new[j].ContainsComplementary(literal):
								complentary_found = True
								break
					# if no complementary found, mark clause to be removed
					if not(complentary_found):
						remove_clauses[i] = True
						removed_flag = True
						break
					complentary_found = False
		print([KB[i] for i in range(KB_len) if not(remove_clauses[i])])

	return [KB[i] for i in range(KB_len) if not(remove_clauses[i])]



def PL_Resolve(ci, cj):
	new_clauses = list()
	
	print('--------------------------------')
	print('-- PL_Resolve')

	print ('Clause 1')
	print (ci)
	print ('Clause 2')
	print (cj)
	
	for i in ci.literals:
		for j in cj.literals:
			listaux = ci.literals + cj.literals
			if Complementary(i,j):
				listaux.remove(i)
				listaux.remove(j)
				new_clause = Clause(listaux)
				if not new_clause.IsTautology():
					new_clauses.append(new_clause)
	
	print('New Clauses')				
	print(new_clauses)
	return new_clauses


def PL_Resolution(KB):
	
	print('--------------------------------')
	print('-- PL_Resolution')

	clauses = list(KB)
	while(True):
	#for n in range (4):
		new = list()
		for clause in combinations(clauses,2):
			resolvents = PL_Resolve(clause[0],clause[1])
		
			# Check if there are any empty clause
			for resolvent in resolvents:
				if resolvent.literals == []:
					#print('True')
					return True
			new = new + resolvents;			
		
		if all(n in clauses for n in new):
			#print("False")
			return False
			
		clauses = new + clauses
		clauses = RemoveImpliedClauses(clauses)

		print (clauses)

def main(argv):

	# get problem from stdin and convert each sentence
	# to clause format, already removes tautologies 
	# and applies factorization
	# for line in sys.stdin:
	# 	if line[0] == '(':
	# 		KB 
	KB = [Clause(eval(line)) for line in sys.stdin if not(Clause(eval(line)).IsTautology())]


	print('--------------------------------')
	print('-- Knowledge Base')
	for clause in KB:
		print(clause)

	# now remove clauses implied by others
	KB = RemoveImpliedClauses(KB)
	print('--------------------------------')
	print('-- RemoveImpliedClauses')
	for clause in KB:
		print(clause)

	KB = Simplify(KB)
	print('--------------------------------')
	print('-- Simplify')
	if KB == []:
		print('empty')
	for clause in KB:
		print(clause)

	if PL_Resolution(KB):
		print('True')
	else:
		print('False')	


if __name__ == "__main__":
	#start_time = time.clock()
	main(sys.argv)

