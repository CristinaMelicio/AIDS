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
		#print([KB[i] for i in range(KB_len) if not(remove_clauses[i])])

	return [KB[i] for i in range(KB_len) if not(remove_clauses[i])]



def PL_Resolve(ci, cj):
	new_clauses = list()
	
	# print('--------------------------------')
	# print('-- PL_Resolve')

	# print ('Clause 1')
	# print (ci)
	# print ('Clause 2')
	# print (cj)
	
	for i in ci.literals:
		for j in cj.literals:
			listaux = list(ci.literals) + list(cj.literals)
			if Complementary(i,j):
				#print(i,j)
				listaux.remove(i)
				listaux.remove(j)
				new_clause = Clause(listaux)
				if not new_clause.IsTautology():
					new_clauses.append(new_clause)
	
	#print('New Clauses')				
	#print(new_clauses)
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
		
		aux = clauses + new
		aux = RemoveImpliedClauses(aux)

		if all(n in clauses for n in aux):
			print("False")
			return False
		# if all(n in clauses for n in new):
		# 	#print("False")
		# 	return False
			
		#clauses = new + clauses
		print(len(clauses))
		#print('RemoveImpliedClauses')
		#clauses = RemoveImpliedClauses(clauses)
		#clauses = Simplify(clauses)
		clauses = Simplify(aux)
		if clauses == []:
			return False
		# for clause in clauses:
		# 	print(clause)
		print(len(clauses))
		#print (clauses)

def PL_Resolution_Unit_Rule(KB):
	
	print('--------------------------------')
	print('-- PL_Resolution_Unit')

	clauses = list(KB)

	while(True):
	#for n in range (4):
		new = list()
		clause_unit = []
		clause_other = []
		for clause in combinations(clauses,2):
			if clause[0].size == 1 or clause[1].size == 1:
				clause_unit.append(clause)
			else: 
				clause_other.append(clause)

		for clause in clause_unit + clause_other:
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
		#print('RemoveImpliedClauses')
		clauses = RemoveImpliedClauses(clauses)
		#print(clauses)
		clauses = Simplify(clauses)
		if clauses == []:
			return False
		#print(clauses)
		print(len(clauses))

def PL_Resolution_Unit_Boost(KB):
	pass

def main(argv):

	# get problem from stdin and convert each line
	# to clause, constructor already applies factorization. 
	KB = []
	if sys.stdin.isatty():
		print('Error - No input file selected')
		return -1

	for line in sys.stdin:
		a = eval(line)
		print(a)
		if line[0] == '(':
			KB.append(Clause([a]))
		else:
			KB.append(Clause(a))

	# because nothing can be always obtained from nothing....
	if len(KB) == 0:
		print('True')
		return 0

	# remove tautologies, if input comes from converter.py
	# this part is redundant. 
	KB = [KB[i] for i in range(len(KB)) if not KB[i].IsTautology()]

	print('--------------------------------')
	print('-- Knowledge Base')
	for clause in KB:
		print(clause)
	print(len(KB))

	# now remove clauses implied by others
	KB = RemoveImpliedClauses(KB)
	print('--------------------------------')
	print('-- RemoveImpliedClauses')
	for clause in KB:
		print(clause)
	print(len(KB))

	print('---------------------------------')

	# remove clauses with literal which complementary is 
	# not present in any other clause, since we would never
	# be able to resolve them
	KB = Simplify(KB)
	print('--------------------------------')
	print('-- Simplify')
	print(len(KB))

	#if no clause is left it means we would never be able
	#to fully resolve to find {}, for this reason the prove is False
	if KB == []:
		print('False')
		return 0

	for clause in KB:
		print(clause)

	# apply resolution algorithm
	if PL_Resolution(KB):
	#if PL_Resolution_Unit_Rule(KB):
		print('True')
	else:
		print('False')	


if __name__ == "__main__":
	#start_time = time.clock()
	main(sys.argv)

