connectors = ['not','and','or','=>','<=>']

# ------------------------------------------------------------
# This part is relevant to work with sentences not yet converted to 
# CNF format

def IsSentenceValid(sentence):
	""" Check if sentence is valid, still needs to be improved"""

	# if sentence has 3 element, first element has to be a connector
	# but in cannot be a negation, also 2 remaining elements cannot be 
	# a connector
	if len(sentence) == 3:
		if not(sentence[0] in connectors) or sentence[0] == 'not' \
		or (sentence[1] in connectors) or (sentence[2] in connectors):
			return False
		return True

	# if sentence has 2 elements it can only be a negation
	# and 2nd element cannot be a connector
	elif len(sentence) == 2:
		if sentence[0] != 'not' or sentence[1] in connectors:
			return False
		return True

	# if sentence has only one element, the element
	# cannot be a connector
	elif len(sentence) == 1:
		if sentence[0] in connectors:
			return False
		return True

	#if sentence has more than 3 elements or less than one it is not valid
	return False

class Sentence(object):
	"""This class represents a logic sentence with the following elements
	connector : first connector that appears in sentence
	args     : everything that comes after the connector """

	def __init__(self, sentence = ['A']):
		# check if sentence uses correct connectors
		if IsSentenceValid(sentence):
			#case it is atomic
			if len(sentence) == 1:
				#print('Instantiate Atom :', sentence)
				self.connector = None
				self.args = sentence[:]
			#all other (including not)
			else:
				#print('Instantiate :', sentence)
				self.connector = sentence[0]
				self.args = sentence[1:]
			##print( 'a' , self.connector, self.args )
		else:
			sys.exit('invalide sentence' , sentence)

	# check if sentence is atomic
	def IsAtom(self):
		if self.connector == None:
			return True
		else:
			return False

	# check if sentence is a negation
	def IsNegation(self):
		if self.connector == 'not':
			return True
		else:
			return False

	# check if sentence is conjunction
	def IsConjunction(self):
		if self.connector == 'and':
			return True
		else:
			return False

	# check if sentence is disjunction
	def IsDisjunction(self):
		if self.connector == 'or':
			return True
		else:
			return False

	# check if sentence is implication
	def IsImplication(self):
		if self.connector == '=>':
			return True
		else:
			return False

	# check if sentence is biconditional
	def IsBiconditional(self):
		if self.connector == '<=>':
			return True
		else:
			return False

	# return sentence as tupple
	def GetSentence(self):
		if self.IsAtom():
			return self.args
		elif self.IsNegation():
			return (self.connector,self.args[0])
		else:
			return (self.connector,self.args[0],self.args[1])

	# parse sentence
	def Parse(self):
		#print( 'Parse : ' , self.connector , self.args )

		# if it is negation only returns one argument
		if self.IsNegation():
			#print('IsN :', self.args )
			return Sentence(self.args[0])

		# else return two sentences, one for each arg
		else :
			return Sentence(self.args[0]), Sentence(self.args[1])

	# return negation of current sentence
	def Negate(self):
		return Sentence(('not', self.GetSentence()))

	# auxiliary for sentence representation for printing
	def __repr__(self):
		if self.IsAtom():
			#return self.args[0]
			return str('\'') + str(self.args[0]) + str('\'')
		elif self.IsNegation():
			return str((self.connector, self.args[0]))
		else:
			return str((self.connector, self.args[0], self.args[1]))

def Conjunction(sentence1,sentence2):
	""" Returns Conjunction of two sentences """
	arg1 = sentence1.GetSentence()
	arg2 = sentence2.GetSentence()
	#print('Conjunction: ', arg1, arg2)
	return Sentence(('and', arg1, arg2))

def Disjunction(sentence1,sentence2):
	""" Returns Disjunction of two sentences """
	arg1 = sentence1.GetSentence()
	arg2 = sentence2.GetSentence()
	#print('Disjunction: ', arg1, arg2)
	return Sentence(('or', arg1, arg2))

def Implication(sentence1,sentence2):
	""" Returns Implication of two sentences """
	arg1 = sentence1.GetSentence()
	arg2 = sentence2.GetSentence()
	#print('Implication: ', arg1, arg2)
	return Sentence(('=>', arg1, arg2))

# ------------------------------------------------------------
# This part is relevant to sentences which where already converted
# to CNF and for this reason can now be represented as conjuctions
# of clauses. Which will make it easier to factorize, remove tautologies
# remove clauses implied by others and afterwards apply resolution
# algorithms


def IsNegation(literal):
	""" Check if literal is negation """

	if literal[0] == 'not':
		return True
	else:
		return False

def Complementary(literal1, literal2):
	""" Check if one literal is negation of the other """

	if IsNegation(literal1):
		if literal1[1] == literal2[0]:
			return True
	elif IsNegation(literal2):
		if literal2[1] == literal1[0]:	
			return True
	return False

class Clause(object):
	"""Clause represents a sentence that only contains disjuctions
	of literals. Because of this propertie we can represent it only as 
	a list of atomic sentences and negations of literals. This representation
	makes it easier to afterwards simplify the sentences by
	removing repetitions, tautologies, etc...
	literals : list of literals that make the sentence, if tautology literals
			   is set to True"""

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

	def __contains__(self, foo):
		if self.size > foo.size:
			return False
		else:
			if all(x in foo.literals for x in self.literals):
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

def ClauseConvert(CNFsentence):
	""" Convert CNF sentence to a list of clauses """

	sentence_list = [CNFsentence]
	clause_list = []
	
	# loop until all conjunctions are eliminated 
	while sentence_list:
		sentence = sentence_list.pop()
		if sentence.IsConjunction():
			sentence1,sentence2 = sentence.Parse()
			sentence_list.append(sentence1)
			sentence_list.append(sentence2)
		else :
			list_literals = ParseDisjunction(sentence)
			clause_list.append(Clause(list_literals))
	return clause_list	

def ParseDisjunction(sentence):
	""" Useful for clause representation, parses disjuction 
	in all its elements which are now only atomic sentences
	or negation of literals, returns list with those elements"""

	to_sparse = [sentence]
	literals = []
	while to_sparse:
		sentence1 = to_sparse.pop()
		if sentence1.IsAtom():
			literals.append(sentence1.GetSentence())
		elif sentence1.IsNegation():
			sentence2 = sentence1.Parse()
			if sentence2.IsAtom():
				literals.append(sentence1.GetSentence())
			else:
				to_sparse.append(sentence2)
		else :
			sentence1,sentence2 = sentence1.Parse()
			to_sparse.append(sentence1)
			to_sparse.append(sentence2)
	return literals	

def RemoveRepeatedClauses(KB):
	""" removes repeated clauses from set of clauses"""
	KB_len = len(KB)
	implied_clauses = [False for i in range(KB_len)]
	checked_clauses = [False for i in range(KB_len)]
	size_clauses = [KB[i].size for i in range(KB_len)]
	possible_sizes = []
	for size in size_clauses: 
		if not(size in possible_sizes):
			possible_sizes.append(size)

	possible_sizes = sorted(possible_sizes)
	i = 0
	for size in possible_sizes:
		for i in range(KB_len):
			if size_clauses[i] == size and not(implied_clauses[i]) and not(checked_clauses[i]):
				checked_clauses[i] = True
				for j in range(KB_len):
					if i!=j and not(implied_clauses[j]) and not(checked_clauses[j]) and KB[j] == KB[i]:
						implied_clauses[j] = True

	return [KB[i] for i in range(KB_len) if not(implied_clauses[i])]

def RemoveImpliedClauses(KB):
	""" returns a new set of clauses from where all
	clauses implied by others were removed (includes removal 
	equal clauses) """

	KB_len = len(KB)
	implied_clauses = [False for i in range(KB_len)]
	checked_clauses = [False for i in range(KB_len)]
	size_clauses = [KB[i].size for i in range(KB_len)]
	possible_sizes = []
	for size in size_clauses: 
		if not(size in possible_sizes):
			possible_sizes.append(size)

	possible_sizes = sorted(possible_sizes)
	i = 0
	for size in possible_sizes:
		for i in range(KB_len):
			if size_clauses[i] == size and not(implied_clauses[i]) and not(checked_clauses[i]):
				checked_clauses[i] = True
				for j in range(KB_len):
					if i!=j and not(implied_clauses[j]) and not(checked_clauses[j]):
						# check if KB[j] is implied by KB[i]
						if KB[j] in KB[i]:
							implied_clauses[j] = True

	return [KB[i] for i in range(KB_len) if not(implied_clauses[i])]
