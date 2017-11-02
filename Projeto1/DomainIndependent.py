
def GeneralSearch(problem, strategy):

	closelist = list()
	strategy.put(problem.initial_state)
	


	flag = True


	while flag:

			
		node = strategy.get()

		if problem.GoalTest(node):
			problem.Traceback(node)

			problem.PrintDecisions()
			problem.PrintEffectiveBF()
			flag = False
			
		else:
			new_nodes = problem.Successor(node)
			for new_node in new_nodes:
				try:
					i = strategy.pq.index(new_node)
					if strategy.pq[i].path_cost > new_node.path_cost:
						strategy.remove(i)
						try:
							closelist.index(new_node)
						except:
							strategy.put(new_node)

				except ValueError:
					strategy.put(new_node)	
			

# def GeneralSearch(problem, strategy):

# 	strategy.put((0,0,problem.initial_state))
# 	flag = True

# 	#for i in range(2):
# 	while flag:
# 		_, _, node = strategy.get()
# 		if problem.GoalTest(node):
# 			problem.Traceback(node)
# 			problem.PrintDecisions()
# 			problem.PrintEffectiveBF()
# 			flag = False
			
# 		else :
# 			new_nodes = problem.Successor(node)

# 			for new_node in new_nodes:
# 				problem.n_nodes = problem.n_nodes + 1
# 				# place on priority queue ordered by path cost
# 				strategy.put((new_node.path_cost, problem.n_nodes, new_node))