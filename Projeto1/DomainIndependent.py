
def GeneralSearch(problem, strategy):

	strategy.put((0,0,problem.initial_state))
	flag = True

	for i in range(1):

		while flag:
			_, _, node = strategy.get()
			if problem.GoalTest(node):
				problem.Traceback(node)
				problem.PrintDecisions()
				flag = False
				
			else :
				new_nodes = problem.Successor(node)

				for new_node in new_nodes:
					problem.n_nodes = problem.n_nodes + 1
					# place on priority queue ordered by path cost
					strategy.put((new_node.path_cost, problem.n_nodes, new_node))