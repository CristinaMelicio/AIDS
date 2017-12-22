import sys
from biblio import *

def main(argv):
	clause_list = []
	for line in sys.stdin:
		a = eval(line)
		#print('-----------------------------------------------')
		#print('-- Sentence to convert')
		#print(a)
		s = Sentence(a)
		##print(s.IsAtom(), s.IsNegation(), s.IsConjunction(), s.IsDisjunction(), s.IsImplication(), s.IsBiconditional())
		cnf_s = CNFConvert(s)
		#print('-----------------------------------------------')
		#print('-- CNF Conversion Result')
		#print(cnf_s)
		#clauses = OutputConvert(cnf_s)
		#print('-----------------------------------------------')
		#print('-- Resultant Clauses')
		#for clause in clauses:
			# only add clauses that are not always True
			#print(clause)

		#print('-----------------------------------------------')
		#print('-- Remove Tautologies and factorize')
		clauses = ClauseConvert(cnf_s)
		for clause in clauses:
			if not(clause.IsTautology()):
				clause_list.append(clause)
				#print(clause)


	#print('-----------------------------------------')
	#for clause in clause_list:
		#print(clause)

	clause_list = RemoveImpliedClauses(clause_list)
	#print('-----------------------------------------')
	for clause in clause_list:
		print(clause)


def CNFConvert(sentence):
	""" Converts recursively sentences to CNF, does not apply simplification rules """

	if sentence.IsAtom():
		return sentence

	elif sentence.IsNegation():
		sentence2 = sentence.Parse()
		if sentence2.IsAtom():
			return sentence
		# double negation
		elif sentence2.IsNegation():
			sentence2 = sentence2.Parse()
			return CNFConvert(sentence2)
		# de Morgan's Law
		elif sentence2.IsConjunction():
			sentence1,sentence2 = sentence2.Parse()
			return CNFConvert(Disjunction(sentence1.Negate(),sentence2.Negate()))
		# de Morgan's Law
		elif sentence2.IsDisjunction():
			sentence1,sentence2 = sentence2.Parse()
			return CNFConvert(Conjunction(sentence1.Negate(),sentence2.Negate()))
		# when argument is implication or biconditional
		else:
			return CNFConvert(CNFConvert(sentence2).Negate())

	elif sentence.IsConjunction():
		sentence1,sentence2 = sentence.Parse()
		sentence1 = CNFConvert(sentence1)
		sentence2 = CNFConvert(sentence2)
		
		return Conjunction(sentence1,sentence2)

	elif sentence.IsDisjunction():
		sentence1,sentence2 = sentence.Parse()
		sentence1 = CNFConvert(sentence1)
		sentence2 = CNFConvert(sentence2)
		# because of the recursivity of CNFConvert
		# if sentence1 and 2 are not conjuctions they can only be
		# disjunctions, atomic sentences or negations of atomic sentences
		# and in this scenario (sentence1 or sentence2) is already CNF format
		if not(sentence1.IsConjunction()) and not(sentence2.IsConjunction()):
			return Disjunction(sentence1,sentence2)
		# if one of them is a conjunction apply Distributive Rule
		else:
			if sentence1.IsConjunction():
				sentence11, sentence12 = sentence1.Parse()
				return CNFConvert(Conjunction(Disjunction(sentence11,sentence2),Disjunction(sentence12,sentence2)))
			elif sentence2.IsConjunction():
				sentence21, sentence22 = sentence2.Parse()
				return CNFConvert(Conjunction(Disjunction(sentence21,sentence1),Disjunction(sentence22,sentence1)))

	elif sentence.IsImplication():
		sentence1,sentence2 = sentence.Parse()
		return CNFConvert(Disjunction(sentence1.Negate(),sentence2))

	elif sentence.IsBiconditional():
		sentence1,sentence2 = sentence.Parse()
		sentence11 = Implication(sentence1,sentence2)
		sentence12 = Implication(sentence2,sentence1)
		return CNFConvert(Conjunction(sentence11,sentence12))

if __name__ == "__main__":
	#start_time = time.clock()
	main(sys.argv)