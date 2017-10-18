from Problem import *
from queue import PriorityQueue


graph = Problem("mir.txt")

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

		# nodes generated in each recursive call of expansion
		virtual_nodes = [node]
		# all nodes derived from the recursive expansion
		new_nodes = []
		while virtual_nodes:
			print('iterou')
			virtual_nodes = expand(virtual_nodes,node)
			for virtual_node in virtual_nodes:
				new_nodes.append(virtual_node)
				virtual_node.print_info()

		for new_node in new_nodes:
			# actualize path_cost with fixed cost
			new_node.path_cost = new_node.path_cost + graph.dict_launch[node.n_launch+1].fixed_cost
			graph.n_nodes = graph.n_nodes +1
			# place on priority queue ordered by path cost
			frontier.put((new_node.path_cost, graph.n_nodes, new_node))

		print_queue(frontier)

def expand(nodes,parent):
	# auxiliary to store already generated states (used for comparsion)
	virtual_states = []
	# stores all new nodes
	new_nodes = []
	# loop trough all received nodes
	for node in nodes:
		possible_components = []
		node.print_info()
		#print('node' , node)

		# collect neighbours of every component in space
		for component in node.state:
			neighbours = graph.dict_comp[component].list_adj
			# verify if the neighbours are already in space or were already added to the list of possible components to lauch
			for neighbour in neighbours:
				if not((neighbour in node.state) or (neighbour in possible_components)):
					possible_components.append(neighbour)	
		print(possible_components)


		for component in possible_components:
			possible_state = list(node.state)
			possible_state.append(component)
			#print('ps', list(node.state), list(node.state).append(component),  possible_state)

			# check if created state already exists
			if not(CheckEqualLists_2(possible_state,virtual_states)):
				# add state to list of current reached states
				virtual_states.append(possible_state)
				payload = graph.dict_comp[component].weight + node.payload
				print(possible_state, payload)
				if( payload < graph.dict_launch[parent.n_launch+1].max_payload):
					print('accepted')
					#print(graph.dict_launch[node.depth+1])
					path_cost = node.path_cost + graph.dict_launch[parent.n_launch+1].var_cost*graph.dict_comp[component].weight
					#print(component, graph.dict_comp[component].vID,  graph.dict_comp[component].weight, graph.dict_comp[component].list_adj, path_cost)
					new_nodes.append(Node(parent = parent, state = possible_state, depth = parent.depth+1, path_cost = path_cost, payload = payload, n_launch = parent.n_launch + 1))
	return new_nodes

# check if a list is equal to one in a set of lists
def CheckEqualLists_2(list1,list_lists):
	for list2 in list_lists:
		if check_equal_lists(list1,list2):
			return True
	return False

# auxiliar to check if two lists are equal
def check_equal_lists(list1,list2):
	for l1 in list1:
		if l1 in list2:
			pass
		else:
			return False
	return True

expand_node(frontier.get()[2])

