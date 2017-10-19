from Problem import *
from queue import PriorityQueue

import cProfile
import re

import time

start_time = time.time()

#graph = Problem("mir.txt")
#graph = Problem("trivial1.txt")
#graph = Problem("trivial2.txt")
#graph = Problem("simple1.txt")
graph = Problem("mir.txt")

def print_queue(queue):
	while not(queue.empty()):
		node = queue.get()[2]
		node.print_info()

def expand_node(node):
	#print('expand ' ,node)
	# all nodes derived from the recursive expansion
	new_nodes = []
	if (node.n_launch+1) in graph.dict_launch:
		# nodes generated in each recursive call of expansion
		virtual_nodes = [node]
		while virtual_nodes:
			#print('iterou')
			virtual_nodes = expand(virtual_nodes,node)
			for virtual_node in virtual_nodes:
				new_nodes.append(virtual_node)
				#virtual_node.print_info()

		for new_node in new_nodes:
			# actualize path_cost with fixed cost
			new_node.path_cost = new_node.path_cost + graph.dict_launch[node.n_launch+1].fixed_cost

		#add empty launch
		new_nodes.append(Node( parent = node, state = node.state, path_cost = node.path_cost, depth = node.depth+1, n_launch = node.n_launch + 1))		
		##print_queue(frontier)

	return new_nodes

def expand(nodes,parent):
	# auxiliary to store already generated states (used for comparsion)
	virtual_states = []
	# stores all new nodes
	new_nodes = []

	# one empty node case
	if nodes[0].state == []:
		node = nodes[0]
		for component in graph.dict_comp:
			if(graph.dict_comp[component].weight <= graph.dict_launch[node.n_launch+1].max_payload):
				#print(graph.dict_comp[component].weight, graph.dict_launch[node.n_launch+1].max_payload)
				state = [component]
				path_cost = node.path_cost + graph.dict_launch[node.n_launch+1].var_cost*graph.dict_comp[component].weight
				##print(component, graph.dict_comp[component].vID,  graph.dict_comp[component].weight, graph.dict_comp[component].list_adj, path_cost)
				new_nodes.append(Node(parent = node, state = state, depth = node.depth+1, path_cost = path_cost, payload = graph.dict_comp[component].weight, n_launch = node.n_launch + 1))

	# other case loop trough all received nodes
	else:
		for node in nodes:
			possible_components = []
			#node.print_info()
			##print('node' , node)

			# collect neighbours of every component in space
			for component in node.state:
				neighbours = graph.dict_comp[component].list_adj
				# verify if the neighbours are already in space or were already added to the list of possible components to lauch
				for neighbour in neighbours:
					if not((neighbour in node.state) or (neighbour in possible_components)):
						possible_components.append(neighbour)	
			#print(possible_components)


			for component in possible_components:
				possible_state = list(node.state)
				possible_state.append(component)
				##print('ps', list(node.state), list(node.state).append(component),  possible_state)

				# check if created state already exists
				if not(CheckEqualLists_2(possible_state,virtual_states)):
					# add state to list of current reached states
					virtual_states.append(possible_state)
					# if node is the parent payload we dont had past payload
					if node == parent:
						payload = graph.dict_comp[component].weight
						#print('node = parent')
					else :
						payload = graph.dict_comp[component].weight + node.payload
						#print(possible_state, payload)
					if( payload <= graph.dict_launch[parent.n_launch+1].max_payload):
						#print(parent.n_launch+1,graph.dict_launch[parent.n_launch+1], payload)
						#print('accepted')
						##print(graph.dict_launch[node.depth+1])
						path_cost = node.path_cost + graph.dict_launch[parent.n_launch+1].var_cost*graph.dict_comp[component].weight
						##print(component, graph.dict_comp[component].vID,  graph.dict_comp[component].weight, graph.dict_comp[component].list_adj, path_cost)
						new_nodes.append(Node(parent = parent, state = possible_state, depth = parent.depth+1, path_cost = path_cost, payload = payload, n_launch = parent.n_launch + 1))

	return new_nodes

explored = []

#print(graph.dict_comp)
#print(graph.dict_launch)

frontier = 	PriorityQueue()
#frontier.put((0,0,Node(state = ['VCM'],payload= graph.dict_comp['VCM'].weight + graph.dict_comp['VK1'].weight )))
frontier.put((0,0,Node()))


flag = True
#for i in range(1):
# while flag:
# 	cost, n_generated, node = frontier.get()
# 	#print('---------------------------------------------------------------------------------------------------------')
# 	#print(cost, n_generated)
# 	#node.print_info()
# 	#print('----------------------------------------------------------------------------------------------------------')
# 	if graph.GoalTest(node):
# 		#print('successsssssssssssssssss')
# 		#node.print_info()
# 		graph.Traceback(node)
# 		flag = False
		
# 	else :
# 		new_nodes = expand_node(node)
# 		for new_node in new_nodes:
# 			#new_node.print_info()
# 			graph.n_nodes = graph.n_nodes +1
# 			# place on priority queue ordered by path cost
# 			frontier.put((new_node.path_cost, graph.n_nodes, new_node))


cProfile.run('re.compile("foo|bar")')


#print("--- %s seconds ---" % (time.time() - start_time))


#print('saiu')

