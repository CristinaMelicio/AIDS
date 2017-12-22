import sys
from biblio import *

def main(argv):
	clause_list = []

	for line in sys.stdin:
		a = eval(line)
		s = Sentence(a)
		cnf_s = CNFConvert(s)
		clauses = ClauseConvert(cnf_s)
		for clause in clauses:
			if not(clause.IsTautology()):
				clause_list.append(clause)
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
		# De Morgan's Law
		elif sentence2.IsConjunction():
			sentence1,sentence2 = sentence2.Parse()
			return CNFConvert(Disjunction(sentence1.Negate(),sentence2.Negate()))
		# De Morgan's Law
		elif sentence2.IsDisjunction():
			sentence1,sentence2 = sentence2.Parse()
			return CNFConvert(Conjunction(sentence1.Negate(),sentence2.Negate()))
		# when argument is implication or biconditional remove them first and 
		# only afterwards negate and try to convert once again
		else:
			return CNFConvert(CNFConvert(sentence2).Negate())

	elif sentence.IsConjunction():
		sentence1,sentence2 = sentence.Parse()
		sentence1 = CNFConvert(sentence1)
		sentence2 = CNFConvert(sentence2)
		# because of the recursivity of CNFConvert
		# when it reaches this point we are sure sentence1 and sentence2
		# are in CNF format, so we can just do the conjunction of both
		return Conjunction(sentence1,sentence2)

	elif sentence.IsDisjunction():
		sentence1,sentence2 = sentence.Parse()
		sentence1 = CNFConvert(sentence1)
		sentence2 = CNFConvert(sentence2)
		# because of the recursivity of CNFConvert
		# if sentence1 and 2 are not conjuctions they can only be
		# disjunctions or literals
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
		# remove implication
		return CNFConvert(Disjunction(sentence1.Negate(),sentence2))

	elif sentence.IsBiconditional():
		sentence1,sentence2 = sentence.Parse()
		sentence11 = Implication(sentence1,sentence2)
		sentence12 = Implication(sentence2,sentence1)
		# remove biconditional
		return CNFConvert(Conjunction(sentence11,sentence12))

if __name__ == "__main__":
	main(sys.argv)
