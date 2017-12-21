import sys
from convert import *
from itertools import combinations

class Clause(object):
	"""Clause represents a sentence that only contains disjuctions
	of literals. Because of this propertie we can represent it only as 
	a list of atomic sentences and negations. This representation
	makes it easier to afterwards simplify the sentences by
	removing repetitions, tautologies, etc...
	literals : list of literals that make the sentence"""

	def __init__(self, list_literals):
		#print('Initialize Clause')
		#print(list_literals)
		self.literals = []
		self.size = 0

		# create clause using simplification rules
		for literal in list_literals:
			# will not add repeated literals to clause
			# and verifies if complementary already exists
			# in clause, if this happens clause is set to True
			# otherwise add literal to clause
			repeated_flag = False
			if IsNegation(literal):
				for literal2 in self.literals:
					if IsNegation(literal2) and literal2[1] == literal[1]:
						repeated_flag = True
						break
					elif literal[1] == literal2[0]:
						self.literals = True	
						break
			else:
				for literal2 in self.literals:
					if IsNegation(literal2) and literal2[1] == literal[0]:
						self.literals = True
						break
					elif literal[0] == literal2[0]:
						repeated_flag = True
						break

			if self.literals == True:
				break

			elif not(repeated_flag):
				self.literals.append(literal)
			
		if self.literals != True:
			self.size = len(self.literals)

		#print(self.literals)
	def IsTautology(self):
		if self.literals == True:
			return True
		else:
			return False

	def Contains(self,literal):
		for i in range(self.size):
			if self.literals[i] == literal:
				return True
		# if literal in self.literals:
		# 	return True
		return False

	def ContainsComplementary(self,literal):
		if IsNegation(literal):
			if literal[1] in self.literals:
				return True
		else:
			if ('not', literal) in self.literals:
				return True


	def __eq__(self, foo):
		if set(self.literals) == set(foo.literals):
			return True
		else:
			return False


	def __repr__(self):
		if self.literals == True:
			return str(True)
		elif self.size == 1:
			if IsNegation(self.literals[0]):
				return str(self.literals[0])
			else:
				return str('\'') + str(self.literals[0]) + str('\'') 
		else:
			return str(self.literals)

def IsNegation(sentence):
	if sentence[0] == 'not':
		return True
	else:
		return False


def IsNegationOf(sentence1, sentence2):
	if IsNegation(sentence1):
		if sentence1[1] == sentence2[0]:
			return True
	elif IsNegation(sentence2):
		if sentence2[1] == sentence1[0]:	
			return True
	return False		

def IsSameLiteral(l1,l2):
	if IsNegation(l1):
		if IsNegation(l2):
			if l1[1] == l2[1]:
				return True
			else:
				return False
		else:
			return False
	else:
		if IsNegation(l2):
			return False
		else:
			if l1[0] == l2[0]:
				return True
			else:
				return False

def Factorize(clause):
	pass

def Tautology(clause):
	pass

def Implies(clause1,clause2):
	""" Tests if clause1 implies clause2"""
	if clause1.size > clause2.size:
		return False
	else:
		for literal1 in clause1.literals:
			literal_found = False
			for literal2 in clause2.literals:
				if IsSameLiteral(literal2,literal1):
					literal_found = True
					break
			if not(literal_found):
				return False				
		return True

def RemoveImpliedClauses(KB):
	""" returns a new set of clauses from where all
	clauses implied by others were removed """

	KB_len = len(KB)
	implied_clauses = [False for i in range(KB_len)]
	checked_clauses = [False for i in range(KB_len)]
	size_clauses = [KB[i].size for i in range(KB_len)]
	possible_sizes = []
	for size in size_clauses: 
		if not(size in possible_sizes):
			possible_sizes.append(size)

	possible_sizes = sorted(possible_sizes)
	#print(size_clauses)
	#print(possible_sizes)
	i = 0
	for size in possible_sizes:
		#print(str('Size : ') + str(size))
		for i in range(KB_len):
			if size_clauses[i] == size and not(implied_clauses[i]) and not(checked_clauses[i]):
				#print(KB[i])
				checked_clauses[i] = True
				for j in range(KB_len):
					if i!=j and not(implied_clauses[j]) and not(checked_clauses[j]):
						if Implies(KB[i],KB[j]):
							implied_clauses[j] = True
							#print(KB[j])

	#print(implied_clauses)
	#print(checked_clauses)
	return [KB[i] for i in range(KB_len) if not(implied_clauses[i])]



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
			if IsNegationOf(i,j):
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

