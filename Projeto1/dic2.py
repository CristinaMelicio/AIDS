from Graph2 import *
from queue import PriorityQueue
from collections import Counter


graph = Graph("mir.txt")

#print(graph.GetDictComponents())

#print(graph.GetDictLaunchs())

explored = []
frontier = []

frontier = 	PriorityQueue()
frontier.put((0,0,Node(state = ['VCM'],payload= graph.dict_comp['VCM'].weight + graph.dict_comp['VK1'].weight )))
#frontier.put((0,0,Node()))

def print_queue(queue):
	while not(queue.empty()):
		node = queue.get()[2]
		node.print_info()

def expand_node(node):
	print(node)
	if node.state == []:
		for component in graph.dict_comp:
			if(graph.dict_comp[component].weight < graph.dict_launch[node.n_launch+1].max_payload):
				graph.n_nodes = graph.n_nodes + 1
				state = [component]
				path_cost = node.path_cost + graph.dict_launch[node.n_launch+1].var_cost*graph.dict_comp[component].weight
				#print(component, graph.dict_comp[component].vID,  graph.dict_comp[component].weight, graph.dict_comp[component].list_adj, path_cost)
				frontier.put((path_cost, graph.n_nodes, Node(parent = node, state = state, depth = node.depth+1, path_cost = path_cost, payload = graph.dict_comp[component].weight, n_launch = node.n_launch)))
		frontier.put((0,0, Node( parent = node, state = ['L'], depth = node.depth+1, n_launch = node.n_launch + 1)))	
		print_queue(frontier)
	else:
		# possible_components = []
		# #verify all components that can be connected to the ones that are already in space
		# for component in node.state:
		# 	# collect all neighbours of a node
		# 	neighbours = graph.dict_comp[component].list_adj
		# 	print(neighbours)
		# 	# verify if the neighbours are already in space or were already added to the list of possible components to lauch
		# 	for neighbour in neighbours:
		# 		if (neighbour in node.state) or (neighbour in possible_components) :
		# 			pass
		# 		else:
		# 			possible_components.append(neighbour)
		# print(possible_components)
		# for component in possible_components:
		# 	virtual_state = list(node.state).append(component)
		# 	payload = graph.dict_comp[component].weight + node.payload
		# 	if( payload < graph.dict_launch[node.n_launch+1].max_payload):
		# 		graph.n_nodes = graph.n_nodes + 1
		# 		state = list(node.state).append(component)
		# 		#print(graph.dict_launch[node.depth+1])
		# 		path_cost = node.path_cost + graph.dict_launch[node.depth+1].var_cost*graph.dict_comp[component].weight
		# 		print(component, graph.dict_comp[component].vID,  graph.dict_comp[component].weight, graph.dict_comp[component].list_adj, path_cost)
		# 		frontier.put((path_cost, graph.n_nodes, Node(parent = node, state = state, depth = node.depth+1, path_cost = path_cost, payload = graph.dict_comp[component].weight)))
		virtual_nodes = [node]
		new_nodes = []
		while virtual_nodes:
			print('iterou')
			virtual_nodes = expand(virtual_nodes,node)
			for virtual_node in virtual_nodes:
				new_nodes.append(virtual_node)
				virtual_node.print_info()
				
		for new_node in new_nodes:
			new_node.path_cost = new_node.path_cost + graph.dict_launch[node.n_launch+1].fixed_cost
			graph.n_nodes = graph.n_nodes +1
			frontier.put((new_node.path_cost, graph.n_nodes, new_node))			
		print_queue(frontier)

def expand(nodes,parent):
	virtual_states = []
	new_nodes = []
	for node in nodes:
		possible_components = []
		node.print_info()
		#print('node' , node)
		for component in node.state:
			# collect all neighbours of a node
			neighbours = graph.dict_comp[component].list_adj
			#print(neighbours)
			# verify if the neighbours are already in space or were already added to the list of possible components to lauch
			for neighbour in neighbours:
				if (neighbour in node.state) or (neighbour in possible_components) :
					pass
				else:
					possible_components.append(neighbour)
		print(possible_components)
		for component in possible_components:
			possible_state = list(node.state)
			possible_state.append(component)
			#print('ps', list(node.state), list(node.state).append(component),  possible_state)
			if check_equal_lists_2(possible_state,virtual_states):
				pass
			else:
				virtual_states.append(possible_state)
				payload = graph.dict_comp[component].weight + node.payload
				print(possible_state, payload)
				if( payload < graph.dict_launch[parent.n_launch+1].max_payload):
					print('a')
					#print(graph.dict_launch[node.depth+1])
					path_cost = node.path_cost + graph.dict_launch[parent.n_launch+1].var_cost*graph.dict_comp[component].weight
					#print(component, graph.dict_comp[component].vID,  graph.dict_comp[component].weight, graph.dict_comp[component].list_adj, path_cost)
					new_nodes.append(Node(parent = parent, state = possible_state, depth = parent.depth+1, path_cost = path_cost, payload = payload, n_launch = parent.n_launch + 1))
	return new_nodes

def check_equal_lists_2(list1,list_lists):
	for list2 in list_lists:
		if check_equal_lists(list1,list2):
			return True
	return False

def check_equal_lists(list1,list2):
	for l1 in list1:
		if l1 in list2:
			pass
		else:
			return False
	return True

expand_node(frontier.get()[2])

