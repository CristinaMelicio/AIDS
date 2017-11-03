
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
			problem.PrintEffectiveBF()
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
			