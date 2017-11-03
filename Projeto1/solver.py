from DomainDependent import *
from DomainIndependent import *
#from queue import PriorityQueue

import time
import timeit

import sys

def main(argv):

	try:																																																																																																																																																														
		problem = Problem(argv[2], argv[1])
	except :
		print("solver.py -i <inputfile> -u <inputfile>")
		sys.exit(2)

	#frontier = 	PriorityQueue()
	frontier = HeapQueue()
	GeneralSearch(problem,frontier)
	
	
	#return(GeneralSearch(problem,frontier))
	
if __name__ == "__main__":
	start_time = time.clock()
	main(sys.argv)
	print(timeit.timeit('"-".join(str(n) for n in range(100))', number=10000))
	print("--- %s seconds ---" % (time.clock() - start_time))

	


