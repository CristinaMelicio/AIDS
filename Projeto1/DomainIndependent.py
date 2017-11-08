
from heapq import *

def GeneralSearch(problem, strategy):

	closedlist = list()
	strategy.put(problem.initial_state)

	while True:
		
		# get node from frontier	
		try:
			node = strategy.get()
			closedlist.append(node)			
		# if frontier empty return failure
		except:
			return str("FAILURE")

		# check if goal state
		if problem.GoalTest(node):
			problem.Traceback(node)
			# problem.PrintEffectiveBF()
			flag = False
			return problem.solution
			
		else:
			# expand node
			new_nodes = problem.Successor(node)
			for new_node in new_nodes:
				# check if successor already in frontier
				try:
					i = strategy.pq.index(new_node)
					# compare nodes evalution functions
					if strategy.pq[i].path_cost > new_node.path_cost:
						# remove old node in frontier
						strategy.remove(i)
						# check if successor already in closed list
						try:
							closedlist.index(new_node)
						except:
							strategy.put(new_node)

				except ValueError:
					strategy.put(new_node)	



class HeapQueue(object):
	
	def __init__(self):
		'Create the open List'
		self.pq = []

	def put(self, task):
		'Add a new task or update the priority of an existing task'
		self.pq.append(task)
		heapify(self.pq)

	def remove(self,index):
		'Remove a task form the priority queue given the index of the position'
		del self.pq[index]
		heapify(self.pq)
		
	def get(self):
		'Return the element with lowest priority task'
		element = heappop(self.pq) 
		return element
