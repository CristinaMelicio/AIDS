from DomainDependent import *
from DomainIndependent import *
#from queue import PriorityQueue
import time
import sys

def main(argv):

	try:																																																																																																																																																														
		problem = Problem(argv[2], argv[1])
	except :
		print("solver.py -i <inputfile> -u <inputfile>")
		sys.exit(2)

	#frontier = 	PriorityQueue()
	frontier = HeapQueue()
	solution = GeneralSearch(problem,frontier)
	if solution == "FAILURE":
		print(solution)
	else :
		for decision in solution:
			print(decision)
	
	#return(GeneralSearch(problem,frontier))
	
if __name__ == "__main__":
	start_time = time.clock()
	main(sys.argv)
	print("--- %s seconds ---" % (time.clock() - start_time))

	


