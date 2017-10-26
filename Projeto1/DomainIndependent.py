
def GeneralSearch(problem, strategy):

	strategy.put(problem.initial_state)
	flag = True

	while flag:
		node = strategy.get()
		if problem.GoalTest(node):
			problem.Traceback(node)
			problem.PrintDecisions()
			flag = False
			
		else:
			new_nodes = problem.Successor(node)
			for new_node in new_nodes:
				problem.n_nodes = problem.n_nodes + 1
				try:
					i = strategy.pq.index(new_node)
					if strategy.pq[i].path_cost > new_node.path_cost:
						strategy.remove(i)
						strategy.put(new_node)
				except ValueError:
					strategy.put(new_node)	
			