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
				self.conector = None
				self.args = sentence
			#all other (including not)
			else:
				self.conector = sentence[0]
				self.args = sentence[1:]
			print 'a' , self.conector, self.args
		else:
			sys.exit('invalide sentence' + sentence)

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

	def Parse(self):
		print 'Parse : ' + self.conector + self.args

		if self.IsNegation():
			print self.args
			return Sentence(self.args)

		else :
			return Sentence(self.args[0]), Sentence(self.args[1])

	def Negate(self):
		return Sentence('not',(self.args[0],self.args[1]))



def ParseAll(sentence):
	print 'ParseAll :' + sentence
	to_sparse = [sentence]
	elements = []
	while to_sparse:
		sentence = to_sparse.pop()
		print 's' + sentence
		if IsAtom(sentence):
			print 'isA'
			elements.append(sentence[])
		elif IsNegation(sentence):
			print 'isN'
			result = sentence.Parse()
			if IsAtom(result):
				elements.append(sentence)
			else:
				to_sparse.append(result)
		else :
			result1,result2 = sentence.Parse()
			print result1, result2
			to_sparse.append(result1)
			to_sparse.append(result2)
	return elements


def CNFConvert(sentence):

	print '---------------------CNF :' + sentence
	if sentence.IsAtom():
		print 'ATO: ' + sentence
		return sentence

	elif sentence.IsNegation() :
		print 'NOT :' + sentence
		sentence2 = sentence.Parse()
		if sentence2.IsAtom():
			print 'NOT/ATOM'
			return sentence
		# double negation
		elif sentence.IsNegation():
			print 'NOT/2NEG'
			sentence2 = sentence2.Parse()
			return CNFConvert(sentence)
		# de Morgan's Law
		elif sentence.IsConjunction():
			print 'NOT/CONJ'
			sentence1,sentence2 = sentence.Parse()
			return CNFConvert(Disjunction(sentence1.Negate(),sentence2.Negate()))
		# de Morgan's Law
		elif sentence.IsDisjunction():
			print 'NOT/DISJ'
			sentence1,sentence2 = sentence.Parse()
			return CNFConvert(Conjunction(sentence1.Negate(),sentence2.Negate()))
		else:
			return Negation(CNFConvert(sentence))

	elif sentence.IsConjunction():
		print 'CON :' + sentence
		sentence1,sentence2 = sentence.Parse()
		sentence1 = CNFConvert(sentence1)
		sentence2 = CNFConvert(sentence2)
		return Conjunction(sentence1,sentence2)

	elif sentence.IsDisjunction():
		print 'DIS :' + sentence
		sentence1,sentence2 = sentence.Parse()
		sentence1 = CNFConvert(sentence1)
		sentence2 = CNFConvert(sentence2)
		print sentence1, sentence2
		if not(sentence1.IsConjunction()) and not(sentence2.IsConjunction()):
			return Disjunction(sentence1,sentence2)
		else:
			if sentence1.IsConjunction():
				sentence11, sentence12 = sentence1.Parse()
				return CNFConvert(Conjunction(Disjunction(sentence11,sentence2),Disjunction(sentence12,sentence2)))
			elif sentence2.IsConjunction():
				sentence21, sentence22 = sentence2.Parse()
				return CNFConvert(Conjunction(Disjunction(sentence21,sentence1),Disjunction(sentence22,sentence1)))

	elif sentence.IsImplication():
		print 'IMP :' + sentence
		sentence1,sentence2 = sentence.Parse()
		return CNFConvert(Disjunction(sentence1.Negate(),sentence2))

	elif sentence.IsBiconditional():
		print 'BIC :' + sentence
		sentence1,sentence2 = sentence.Parse()
		return CNFConvert(Conjunction(Implication(sentence1,sentence2),Implication(sentence2,sentence1)))
