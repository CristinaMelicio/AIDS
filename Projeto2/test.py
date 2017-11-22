CNF_result = []
import re		


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

def SentenceParse(sentence):
	# number_tupples = sentence.count('(')
	# print(number_tupples)

	print 'Parse : ' + sentence
	try :
		begin = sentence.index(',')
		end   = sentence.rindex(')')
		args  = sentence[begin+2:end]
		print(args)

	except :
		return False

	if IsNegation(sentence):
		#print(args)
		return args

	n = 0
	for i in range(len(args)):
		element = args[i]
		if element == '(':
			n = n+1
		elif element == ')':
			n = n-1
		elif element == ',' and n == 0:
			#print(args[:i],args[i+2:])
			return args[:i], args[i+2:]

def Negation(arg1):
	return "('not', " + arg1 + ')'


def Conjunction(arg1,arg2):
	return "('and', " + arg1 + ", " + arg2 + ')'


def Disjunction(arg1,arg2):
	return "('or', " + arg1 + ", " + arg2 + ')'

def CheckConjunctions(arg):
	return arg.count('and')

def ParseAll(arg):
	print 'ParseAll :' + arg
	to_sparse = [arg]
	elements = []
	while to_sparse:
		sentence = to_sparse.pop()
		print 's' + sentence
		if IsAtom(sentence):
			print 'isA'
			elements.append(sentence)
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
		conj_arg1 = CheckConjunctions(arg1)
		conj_arg2 = CheckConjunctions(arg2)
		arg1_parsed = ParseAll(arg1)
		arg2_parsed = ParseAll(arg2)
		lista = []
		for a in arg1_parsed:
			for b in arg2_parsed:
				if a != b:
					lista.append(Disjunction(a,b))
					try:
						result = Conjunction(result,Disjunction(a,b))
					except:
						result = Disjunction(a,b)
		print  result
		return result
	
	elif IsImplication(sentence):
		print 'IMP :' + sentence
		arg1,arg2 = SentenceParse(sentence)
		return CNFConvert(Disjunction(Negation(arg1),arg2))

	elif IsBiconditional(sentence):
		print 'BIC :' + sentence
		arg1,arg2 = SentenceParse(sentence)
		return CNFConvert(Disjunction(Conjunction(arg1,Negation(arg2)),
									  Conjunction(Negation(arg1),arg2)))
	# else:
	# 	return 'error'



		
fname = 'test2.txt'
f = open(fname,'r')
for line in f: 
	print(str(line))
	print(IsAtom(line), IsNegation(line),IsConjunction(line), IsDisjunction(line), IsImplication(line),IsBiconditional(line))
	print'---------------------CNF----------------------'
	print CNFConvert(line)
	print'-----------------------------------------------'
	# parts = re.split(',',line)
	# for part in parts:
	# 	print(part)
