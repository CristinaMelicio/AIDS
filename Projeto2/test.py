import sys


CNF_result = []

### Verify type of sentence 

def IsAtom(sentence):
	try:
		if sentence[0] != '(' and sentence[-1] != ')':
			return True
		else :
			return False
	except:
		return False

def IsNegation(sentence):
	try:
		if sentence[2:5] == 'not':
			return True
		else :
			return False
	except:
		return False

def IsConjunction(sentence):
	try:
		if sentence[2:5] == 'and':
			return True
		else :
			return False
	except:
		return False

def IsDisjunction(sentence):
	try:
		if sentence[2:4] == 'or':
			return True
		else :
			return False
	except:
		return False

def IsImplication(sentence):
	try:
		if sentence[2:4] == '=>':
			return True
		else :
			return False
	except:
		return False

def IsBiconditional(sentence):
	try:
		if sentence[2:5] == '<=>':
			return True
		else :
			return False
	except:
		return False

def Negation(arg1):
	return "('not', " + arg1 + ')'


def Conjunction(arg1,arg2):
	return "('and', " + arg1 + ", " + arg2 + ')'


def Disjunction(arg1,arg2):
	return "('or', " + arg1 + ", " + arg2 + ')'

def Implication(arg1,arg2):
	return "('=>', " + arg1 + ', '+ arg2 + ')'

def IsComplementary(arg1,arg2):
	if Negation(arg1) == arg2 or Negation(arg2) == arg1:
		return True
	else:
		return False

def SentenceParse(sentence):

	print 'Parse : ' + sentence
	try :
		begin = sentence.index(',')
		end   = sentence.rindex(')')
		args  = sentence[begin+2:end]
		print(args)

	except :
		return False

	if IsNegation(sentence):
		print(args)
		return args

	n = 0
	for i in range(len(args)):
		element = args[i]
		if element == '(':
			n = n+1
		elif element == ')':
			n = n-1
		elif element == ',' and n == 0:
			print(args[:i],args[i+2:])
			return args[:i], args[i+2:]

def ParseAll(arg):
	print 'ParseAll :' + arg
	to_sparse = [arg]
	elements = []
	while to_sparse:
		sentence = to_sparse.pop()
		print 's' + sentence
		if IsAtom(sentence):
			print 'isA'
			elements.append(sentence[])
		elif IsNegation(sentence):
			print 'isN'
			result = SentenceParse(sentence)
			if IsAtom(result):
				elements.append(sentence)
			else:
				to_sparse.append(result)
		else :
			result1,result2 = SentenceParse(sentence)
			print result1, result2
			to_sparse.append(result1)
			to_sparse.append(result2)
	return elements





def CNFConvert(sentence):

	print '---------------------CNF :' + sentence
	if IsAtom(sentence):
		print 'ATO: ' + sentence
		return sentence

	elif IsNegation(sentence):
		print 'NOT :' + sentence
		arg = SentenceParse(sentence)
		if IsAtom(arg):
			print 'NOT/ATOM'
			return sentence
		# double negation
		elif IsNegation(arg):
			print 'NOT/2NEG'
			arg = SentenceParse(arg)
			return CNFConvert(arg)
		# de Morgan's Law
		elif IsConjunction(arg):
			print 'NOT/CONJ'
			arg1,arg2 = SentenceParse(arg)
			return CNFConvert(Disjunction(Negation(arg1),Negation(arg2)))
		# de Morgan's Law
		elif IsDisjunction(arg):
			print 'NOT/DISJ'
			arg1,arg2 = SentenceParse(arg)
			return CNFConvert(Conjunction(Negation(arg1),Negation(arg2)))
		else:
			return Negation(CNFConvert(arg))

	elif IsConjunction(sentence):
		print 'CON :' + sentence
		arg1,arg2 = SentenceParse(sentence)
		arg1 = CNFConvert(arg1)
		arg2 = CNFConvert(arg2)
		return Conjunction(arg1,arg2)

	elif IsDisjunction(sentence):
		print 'DIS :' + sentence
		arg1,arg2 = SentenceParse(sentence)
		arg1 = CNFConvert(arg1)
		arg2 = CNFConvert(arg2)
		print arg1, arg2
		if not(IsConjunction(arg1)) and not(IsConjunction(arg2)):
			return Disjunction(arg1,arg2)
		else:
			if IsConjunction(arg1):
				arg11, arg12 = SentenceParse(arg1)
				return CNFConvert(Conjunction(Disjunction(arg11,arg2),Disjunction(arg12,arg2)))
			elif IsConjunction(arg2):
				arg21, arg22 = SentenceParse(arg2)
				return CNFConvert(Conjunction(Disjunction(arg21,arg1),Disjunction(arg22,arg1)))
			# arg1_parsed = ParseAll(arg1)
			# arg2_parsed = ParseAll(arg2)
			# lista = []
			# for a in arg1_parsed:
			# 	for b in arg2_parsed:
			# 		if a != b :
			# 			lista.append(Disjunction(a,b))
			# 			try:
			# 				result = Conjunction(result,Disjunction(a,b))
			# 			except:
			# 				result = Disjunction(a,b)
			# print  result
			# return result
	
	elif IsImplication(sentence):
		print 'IMP :' + sentence
		arg1,arg2 = SentenceParse(sentence)
		return CNFConvert(Disjunction(Negation(arg1),arg2))

	elif IsBiconditional(sentence):
		print 'BIC :' + sentence
		arg1,arg2 = SentenceParse(sentence)
		#return CNFConvert(Disjunction(Conjunction(arg1,Negation(arg2)),
		#							  Conjunction(Negation(arg1),arg2)))
		return CNFConvert(Conjunction(Implication(arg1,arg2),Implication(arg2,arg1)))
	# else:
	# 	return 'error'

def GetClauses(CNFsentence):
	sentence_list = [CNFsentence]
	clause_list = []
	while sentence_list:
		sentence = sentence_list.pop()
		if IsConjunction(sentence):
			sentence1,sentence2 = SentenceParse(sentence)
			sentence_list.append(sentence1)
			sentence_list.append(sentence2)
		else :
			clause_list.append(sentence)
	return clause_list		

class Clause(object):
	def __init__(self, sentence):
		list_variables = ParseAll(sentence)
		self.list = []
		for variable1 in list_variables:
			if not(variable1 in self.list):
				if IsNegation(variable1):
					for variable2 in list_variables:
						if Negation(variable2) == variable1:
							self.list = True
							break
					if self.list == True:
						break
					else:
						self.list.append(variable1)
				elif not(Negation(variable1) in list_variables):
					self.list.append(variable1)
		print self.list
		self.size = sentence.count('or') + 1
		self.n_not = sentence.count('not')

		
#fname = 'test.txt'
#f = open(fname,'r')
for line in sys.stdin:
	print(line)
	line = line.replace("\n\r", "")
	print(IsAtom(line), IsNegation(line),IsConjunction(line), IsDisjunction(line), IsImplication(line),IsBiconditional(line))
	print'---------------------CNF----------------------'
	CNFConvert =  CNFConvert(line)
	print CNFConvert
	print'-----------------------------------------------'
	GetClauses = GetClauses(CNFConvert)
	print'-----------------------------------------------'
	for clause in GetClauses:
		print clause
		new_clause = Clause(clause)
	print'-----------------------------------------------'
	# parts = re.split(',',line)
	# for part in parts:
	# 	print(part)
