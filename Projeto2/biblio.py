connectors = ['not','and','or','=>','<=>']

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



def CNFConvert(sentence):
	""" Converts sentence to CNF, does not any simplification rule """

	#print('---------------------CNF :',sentence)
	if sentence.IsAtom():
		#print('ATO: ', sentence)
		return sentence

	elif sentence.IsNegation():
		#print( 'NOT :' , sentence )
		sentence2 = sentence.Parse()
		#print('s2 :' , sentence2)
		if sentence2.IsAtom():
			#print( 'NOT/ATOM' )
			return sentence
		# double negation
		elif sentence2.IsNegation():
			#print( 'NOT/2NEG' )
			sentence2 = sentence2.Parse()
			return CNFConvert(sentence2)
		# de Morgan's Law
		elif sentence2.IsConjunction():
			#print( 'NOT/CONJ' )
			sentence1,sentence2 = sentence2.Parse()
			return CNFConvert(Disjunction(sentence1.Negate(),sentence2.Negate()))
		# de Morgan's Law
		elif sentence2.IsDisjunction():
			#print( 'NOT/DISJ' )
			sentence1,sentence2 = sentence2.Parse()
			return CNFConvert(Conjunction(sentence1.Negate(),sentence2.Negate()))
		else:
			#print( 'NOT/ELSE' )
			return CNFConvert(CNFConvert(sentence2).Negate())

	elif sentence.IsConjunction():
		#print( 'CON :' , sentence )
		sentence1,sentence2 = sentence.Parse()
		sentence1 = CNFConvert(sentence1)
		sentence2 = CNFConvert(sentence2)
		#print( 'CON again:', sentence, sentence1, sentence2 )
		return Conjunction(sentence1,sentence2)

	elif sentence.IsDisjunction():
		#print( 'DIS :' , sentence )
		sentence1,sentence2 = sentence.Parse()
		sentence1 = CNFConvert(sentence1)
		sentence2 = CNFConvert(sentence2)
		#print( 'DIS again:', sentence, sentence1, sentence2 )
		if not(sentence1.IsConjunction()) and not(sentence2.IsConjunction()):
			return Disjunction(sentence1,sentence2)
		else:
			if sentence1.IsConjunction():
				#print('IsCon s1')
				sentence11, sentence12 = sentence1.Parse()
				return CNFConvert(Conjunction(Disjunction(sentence11,sentence2),Disjunction(sentence12,sentence2)))
			elif sentence2.IsConjunction():
				#print('IsCon s2')
				sentence21, sentence22 = sentence2.Parse()
				return CNFConvert(Conjunction(Disjunction(sentence21,sentence1),Disjunction(sentence22,sentence1)))

	elif sentence.IsImplication():
		#print( 'IMP :' , sentence )
		sentence1,sentence2 = sentence.Parse()
		return CNFConvert(Disjunction(sentence1.Negate(),sentence2))

	elif sentence.IsBiconditional():
		#print( 'BIC :' , sentence )
		sentence1,sentence2 = sentence.Parse()
		#print('s1,s2 :', sentence1,sentence2)
		sentence11 = Implication(sentence1,sentence2)
		sentence12 = Implication(sentence2,sentence1)
		#print('s11,s12 :', sentence11, sentence12)
		return CNFConvert(Conjunction(sentence11,sentence12))
		#return CNFConvert(Conjunction(Implication(sentence1,sentence2),Implication(sentence2,sentence1)))


class Clause(object):
	"""Clause represents a sentence that only contains disjuctions
	of literals. Because of this propertie we can represent it only as 
	a list of atomic sentences and negations. This representation
	makes it easier to afterwards simplify the sentences by
	removing repetitions, tautologies, etc...
	literals : list of literals that make the sentence"""

	def __init__(self, sentence):
		# parse sentence in all its elements
		#print(sentence)
		list_literals = ParseConjunction(sentence)
		self.literals = []
		self.size = 0

		# create clause using simplification rules
		for literal in list_literals:
			# will not add repeated literals to clause
			# and verifies if complementary already exists
			# in clause, if this happens clause is set to True
			# otherwise add literal to clause
			repeated_flag = False
			if literal.IsNegation():
				for literal2 in self.literals:
					if literal.args[0] == literal2.args[0]:
						if literal2.IsNegation():
							repeated_flag = True
						else:
							self.literals = True	
						break
			else:
				for literal2 in self.literals:
					if literal.args[0] == literal2.args[0]:
						if literal2.IsNegation():
							self.literals = True
						else:
							repeated_flag = True
						break

			if self.literals == True:
				break

			elif not(repeated_flag):
				self.literals.append(literal)
				self.size += 1

		#print(self.literals)

	def Contains(self,clause):
		#print(self.literals,clause.literals)
		if self.size > clause.size:
			return False

		for literal in clause.literals :
			if not(literal in self.literals):
				#print('s', literal)
				return False
		return True

	def __repr__(self):
		if self.literals == True:
			return str(True)
		elif len(self.literals) == 1: 
			return str(self.literals[0])
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
			clause_list.append(Clause(sentence))
	return clause_list	

def OutputConvert(CNFsentence):

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
			list_literals = ParseConjunction(sentence)
			clause_list.append(list_literals)
	return clause_list	


def ParseConjunction(sentence):
	""" Useful for clause representation, parses conjuction 
	in all its elements which are now only atomic sentences
	or negations, returns list with those elements"""

	#print('ParseConjunction :', sentence)
	to_sparse = [sentence]
	literals = []
	while to_sparse:
		sentence1 = to_sparse.pop()
		#print( 's :', sentence1)
		if sentence1.IsAtom():
			#print('isA')
			literals.append(sentence1)
		elif sentence1.IsNegation():
			#print('isN')
			sentence2 = sentence1.Parse()
			if sentence2.IsAtom():
				literals.append(sentence1)
			else:
				to_sparse.append(sentence2)
		else :
			sentence1,sentence2 = sentence1.Parse()
			#print(sentence1, sentence2)
			to_sparse.append(sentence1)
			to_sparse.append(sentence2)
	return literals

