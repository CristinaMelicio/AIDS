from Problem import *
from DomainIndependent import *
from queue import PriorityQueue
import time
import sys


start_time = time.clock()
mode = 'U'

problem = Problem("rui.txt")

def print_queue(queue):
	while not(queue.empty()):
		node = queue.get()[2]
		node.print_info()

frontier = 	PriorityQueue()

GeneralSearch(problem,frontier)

print("--- %s seconds ---" % (time.clock() - start_time))
#print('saiu')

