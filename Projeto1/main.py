from Problem import *
from queue import PriorityQueue
import time
from DomainIndependent import *


problem = Problem("simple1.txt")

def print_queue(queue):
	while not(queue.empty()):
		node = queue.get()[2]
		node.print_info()

frontier = 	PriorityQueue()

GeneralSearch(problem,frontier)

print(time.clock())

#print('saiu')

