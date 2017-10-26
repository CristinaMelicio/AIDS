
from heapq import *

class HeapQueue(object):
	
	def __init__(self):
		self.pq = []

	def put(self, task):
		#'Add a new task or update the priority of an existing task'
		self.pq.append(task)
		heapify(self.pq)

	def remove(self,index):
		#'Mark an existing task as REMOVED.  Raise KeyError if not found.'
		del self.pq[index]
		heapify(self.pq)
		
	def get(self):
		#'Remove and return the lowest priority task. Raise KeyError if empty.'	
		element = heappop(self.pq) 
		return element
			
			
			
			
