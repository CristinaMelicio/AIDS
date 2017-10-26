from DomainDependent import *
from DomainIndependent import *
#from queue import PriorityQueue
import time
import sys, getopt
from Heap import *

def main(argv):
	try:																																																																																																																																																														
		problem = Problem(sys.argv[2], sys.argv[1])
	except :
		print("solver.py -i <inputfile> -u <inputfile>")
		sys.exit(2)

	#frontier = 	PriorityQueue()
	
	#GeneralSearch(problem,frontier)
	frontier = HeapQueue()
	GeneralSearch(problem,frontier)
		

if __name__ == "__main__":
	start_time = time.clock()
	main(sys.argv[1:])
	print("--- %s seconds ---" % (time.clock() - start_time))


