conectors = ['not','and','or','=>','<=>']

#Needs to be improved
def IsSentenceValid(sentence):
	if len(sentence) == 3:
		if not(sentence[0] in conectors) or (sentence[1] in conectors) or (sentence[2] in conectors):
			return False
		return True

	elif len(sentence) == 2:
		if sentence[0] != 'not' or sentence[1] in conectors:
			return False
		return True

	elif len(sentence) == 1:
		if sentence[0] in conectors:
			return False
		return True

	return False

class Sentence(object):
	"""docstring for ClassName"""
	def __init__(self, sentence = ['A']):
		if IsSentenceValid(sentence):
			#case it is atomic
			if len(sentence) == 1:
				#print('Instantiate Atom :', sentence)
				self.conector = None
				self.args = sentence
			#all other (including not)
			# elif len(sentence) == 2:
			# 	#print('Neg :', sentence)
			# 	self.conector = sentence[0]
			# 	self.args = sentence[1]
			else:
				#print('Instantiate :', sentence)
				self.conector = sentence[0]
				self.args = sentence[1:]
			##print( 'a' , self.conector, self.args )
		else:
			sys.exit('invalide sentence' , sentence)

	def IsAtom(self):
		if self.conector == None:
			return True
		else:
			return False

	def IsNegation(self):
		if self.conector == 'not':
			return True
		else:
			return False

	def IsConjunction(self):
		if self.conector == 'and':
			return True
		else:
			return False

	def IsDisjunction(self):
		if self.conector == 'or':
			return True
		else:
			return False

	def IsImplication(self):
		if self.conector == '=>':
			return True
		else:
			return False

	def IsBiconditional(self):
		if self.conector == '<=>':
			return True
		else:
			return False

	def GetSentence(self):
		if self.IsAtom():
			return self.args
		elif self.IsNegation():
			return (self.conector,self.args[0])
		else:
			return (self.conector,self.args[0],self.args[1])

	def Parse(self):
		#print( 'Parse : ' , self.conector , self.args )

		if self.IsNegation():
			#print('IsN :', self.args )
			return Sentence(self.args[0])

		else :
			return Sentence(self.args[0]), Sentence(self.args[1])

	def Negate(self):
		return Sentence(('not', self.GetSentence()))

	def __repr__(self):
		if self.IsAtom():
			return(str(self.args))
		elif self.IsNegation():
			return str((self.conector, self.args[0]))
		else:
			return str((self.conector,self.args[0],self.args[1]))

def Conjunction(sentence1,sentence2):
	arg1 = sentence1.GetSentence()
	arg2 = sentence2.GetSentence()
	#print('Conjunction: ', arg1, arg2)
	return Sentence(('and', arg1, arg2))

def Disjunction(sentence1,sentence2):
	arg1 = sentence1.GetSentence()
	arg2 = sentence2.GetSentence()
	#print('Disjunction: ', arg1, arg2)
	return Sentence(('or', arg1, arg2))

def Implication(sentence1,sentence2):
	arg1 = sentence1.GetSentence()
	arg2 = sentence2.GetSentence()
	#print('Implication: ', arg1, arg2)
	return Sentence(('=>', arg1, arg2))

def CNFConvert(sentence):

	#print('---------------------CNF :',sentence)
	if sentence.IsAtom():
		#print('ATO: ', sentence)
		return sentence

	elif sentence.IsNegation() :
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



def ParseAll(sentence):
	#print('ParseAll :', sentence)
	to_sparse = [sentence]
	symbols = []
	while to_sparse:
		sentence1 = to_sparse.pop()
		#print( 's :', sentence1)
		if sentence1.IsAtom():
			#print('isA')
			symbols.append(sentence1)
		elif sentence1.IsNegation():
			#print('isN')
			sentence2 = sentence1.Parse()
			if sentence2.IsAtom():
				symbols.append(sentence1)
			else:
				to_sparse.append(sentence2)
		else :
			sentence1,sentence2 = sentence1.Parse()
			#print(sentence1, sentence2)
			to_sparse.append(sentence1)
			to_sparse.append(sentence2)
	return symbols

def GetClauses(CNFsentence):
	sentence_list = [CNFsentence]
	clause_list = []
	while sentence_list:
		sentence = sentence_list.pop()
		if sentence.IsConjunction():
			sentence1,sentence2 = sentence.Parse()
			sentence_list.append(sentence1)
			sentence_list.append(sentence2)
		else :
			clause_list.append(sentence)
	return clause_list		

class Clause(object):
	"""docstring for Clause"""
	def __init__(self, sentence):
		list_symbols = ParseAll(sentence)
		self.symbols = []
		for symbol in list_symbols:
			if not(symbol in self.symbols):
				if symbol.IsNegation():
					for symbol2 in list_symbols:
						if (symbol2.args[0] == symbol.args[0]) and (symbol2 != symbol):
							self.symbols = True
							break
					if self.symbols == True:
						break
					else:
						self.symbols.append(str(symbol.GetSentence()))
					#self.symbols.append(symbol)
				elif not(symbol.Negate() in list_symbols):
					self.symbols.append(str(symbol.GetSentence()))
		print(self.symbols)

	def Contains(self,clause):
		#print(self.symbols,clause.symbols)
		for symbol in clause.symbols :
			if not(symbol in self.symbols):
				#print('s', symbol)
				return False
		return True

	def __repr__(self):
		return str(self.symbols)
