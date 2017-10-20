from Problem import *
from DomainIndependent import *
from queue import PriorityQueue
import time
import sys, getopt


def print_queue(queue):
	while not(queue.empty()):
		node = queue.get()[2]
		node.print_info()

def main(argv):
	inputfile = ''
	try:
		opts, args = getopt.getopt(argv,"hi:u:",["ifile="])
	except getopt.GetoptError:
		print("solver.py -i <inputfile> -u <inputfile>")
		sys.exit(2)
		
	for opt, arg in opts:
		if opt == '-h':
			print("solver.py -i <inputfile> -u <inputfile>")
			sys.exit()
		
	problem = Problem(sys.argv[2], sys.argv[1])
		
	frontier = 	PriorityQueue()

	GeneralSearch(problem,frontier)
	

if __name__ == "__main__":
	start_time = time.clock()
	main(sys.argv[1:])
	print("--- %s seconds ---" % (time.clock() - start_time))


