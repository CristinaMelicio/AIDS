import sys
from convert import *

def main(argv):
	for line in sys.stdin:
		a = eval(line)
		print a
		# for element in a:
		# 	print element
		s = Sentence(a)
		print s.IsAtom(), s.IsNegation(), s.IsConjunction(), s.IsDisjunction(), s.IsImplication(), s.IsBiconditional()


if __name__ == "__main__":
	#start_time = time.clock()
	main(sys.argv)