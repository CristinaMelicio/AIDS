from heapq import *
from math import exp, log1p
import datetime


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

class Component(object):

	def __init__(self, vID = None, weight = 0):
		'Create a Component with ID name, weight and a list of adjacence'
	
		self.vID = vID 
		self.weight = weight
		self.list_adj = []

	def SetAdjacents(self, vIDadj):
		self.list_adj.append(vIDadj)

	def SetWeight(self, weight):
		self.weight = weight

	def __repr__(self):
		return "W= " + str(self.weight) + " " + "A= " + str(self.list_adj) + "\n"

class Launch(object):
	
	def __init__(self, dateID = None, max_payload = 0, fixed_cost = 0, var_cost = 0):
		'Create a Launch w/ the send date, maximum payload, fixed cost and the variable cost'

		self.dateID = dateID
		self.max_payload = max_payload
		self.fixed_cost = fixed_cost
		self.var_cost = var_cost
		
		# to help in the heuristics the cost density
		if(max_payload != 0):
			self.cost_density = (fixed_cost+var_cost*max_payload)/max_payload
		else:
			self.cost_density = float("inf")

	def SetIDdate(self, dateID):
		self.dateID = dateID

	def SetMaxPayload(self, max_payload):
		self.max_payload = max_payload

	def SetFixedCost(self, fixed_cost):
		self.fixed_cost = fixed_cost

	def SetVarCost(self, var_cost):
		self.var_cost = var_cost

	def __repr__(self):
		return str(self.dateID) + '  ' + str(self.max_payload) + "," +  str(self.fixed_cost) + "," +  str(self.var_cost) + "," + str(self.cost_density) + "\n" 	

class Problem(object):

	
	def __init__(self, file, mode = None):
		'Create a problem formulation from a text file'	

		# mode uniformed / informed
		self.mode = mode	
		# dictionary of components
		self.dict_comp = {}
		# dicionary of launches (ordered by date, key goes from 1 to number of launches)
		self.dict_launch = {}
		# number expanded nodes
		self.n_expanded = 0
		# number generated nodes
		self.nodes_generated = 0
		# decisions to be made
		self.decisions = []
		# total cost
		self.final_cost = 0
		# depth of solution
		self.final_depth = 0
		# initial state
		self.initial_state = Node()		
		
		# choose function to calculate the cost
		# uninformed search only consider the path cost
		if mode == '-u':
			self.func = self.PathCostFunc
		# informed search consider the path cost plus the heuristic
		# evaluation function
		elif mode == '-i':
			self.func = self.EvaluationFunc
			
		# open the txt file	
		try:
			file = open(file, "r")
		except IOError:
			print ("ERROR: There is not such a file")
			exit()

		# reading each line searching for V, E and L
		for line in file:
			
			# "V" correspond to a component with a weigth
			# if that component is already at the component dictionary we only add the weigth
			# if not we create a new key
			if line[0] == 'V':
				line = line.strip('\n')
				comp_id = line.split(None, 1)[0]
				comp_w  = float(line.split(None, 1)[1])			
				try: 
					self.dict_comp[comp_id].SetWeight(comp_w)
				except:
					self.dict_comp[comp_id] = Component(comp_id, comp_w)

			# "E" correspond to a edge therefore the list of adjacency of a component is extracted
			# if the first component is already a key of the component dictionary, the second componet is added 
			# to the adjacent list
			# if it is not we create a new key with the first and put the second in the adjacency list 
			# we also see if the second component is a key and add the first component to the adjacency list
			# if not it is added
			elif line[0] == 'E':
				line = line.strip('\n')	
				comp_id1 = line.split()[1]
				comp_id2 = line.split()[2]
				try:
					self.dict_comp[comp_id1].SetAdjacents(comp_id2)
				except:
					self.dict_comp[comp_id1] = Component(comp_id1)
					self.dict_comp[comp_id1].SetAdjacents(comp_id2)
				try:
					self.dict_comp[comp_id2].SetAdjacents(comp_id1)
				except:
					self.dict_comp[comp_id2] = Component(comp_id2)
					self.dict_comp[comp_id2].SetAdjacents(comp_id1)

			# "L" correspond to a launch therefore we create a launch object per each line 
			# and put it in the launch dictionary than we sort it in chronological order
			# the date is the key
			elif line[0] == 'L':
				line = line.strip('\n')
				date_id = datetime.datetime.strptime(line.split()[1], '%d%m%Y').date()
				max_payload = float(line.split()[2])
				fixed_cost = float(line.split()[3])
				var_cost = float(line.split()[4])
				self.dict_launch[date_id] = Launch(date_id, max_payload, fixed_cost, var_cost)

		file.close()
		
		list_aux = sorted(self.dict_launch.items(), key=lambda t: t[0])		
		dict_aux = {}
		for i in range(len(list_aux)):
			dict_aux[i+1] = list(list_aux[i])[1]	
		self.dict_launch = dict_aux	

	def GoalTest(self, node):
		'Checks if all elements are already in space'
	
		# saves the final cost and depth of the goal solution
		if set(node.state) == set(self.dict_comp.keys()):
			self.final_cost = node.path_cost
			self.final_depth = node.depth
			return True
		else:
			return False

	def Traceback(self, node):
		'Traces all the decisions made from the goal state until the initial node'
		
		while not (node.state == []):
			dif_components = set(node.state) - set(node.parent.state)
			dif_costs = round(node.path_cost-node.parent.path_cost - node.heuristic + node.parent.heuristic,6)
			
			#don t save the empty launches
			if node.payload != 0:
				self.decisions.append(self.dict_launch[node.depth].dateID.strftime('%d%m%Y') 
									+ ' ' + ' '.join(dif_components) + ' ' + str(dif_costs))
			node = node.parent

	def PrintDecisions(self):
		'Print the decisions from the traceback function since initial state until the goal state'
		
		for i in range(len(self.decisions)):
			print(self.decisions[-(i+1)])
		print(round(self.final_cost,6))

	def Successor(self, node):
		'Sucessor Function '
	
		# all nodes derived from the recursive expansion
		new_nodes = []
		self.n_expanded = self.n_expanded + 1

		# only expand if theres is enough payload available in the next launches
		if self.CheckPossiblePayload(node) == True:
			# not expand last node
			if (node.depth + 1) in self.dict_launch:
				# nodes generated in each recursive call of expansion
				virtual_nodes = [node]
				while virtual_nodes:
					virtual_nodes = self.Expand(virtual_nodes, node)
					for virtual_node in virtual_nodes:
						new_nodes.append(virtual_node)
				# for each node expanded update the cost function
				for new_node in new_nodes:
					new_node.path_cost = self.func(new_node, node)
					self.nodes_generated = self.nodes_generated + 1

				# add empty launch it means same state from node before
				null_node = Node(parent = node, state = node.state, 
										path_cost = node.path_cost, 
										depth = node.depth+1)
				null_node.path_cost = self.func(null_node,node) - self.dict_launch[null_node.depth].fixed_cost

				new_nodes.append(null_node)
				self.nodes_generated = self.nodes_generated + 1

		return new_nodes

	def Expand(self, nodes, parent):
		'Auxiliary function to expand nodes'
		
		# auxiliary list to store already generated states (used for comparsion)
		virtual_states = []
		# stores all new nodes
		new_virtual_nodes = []

		# case of one empty node case
		if nodes[0].state == []:
			node = nodes[0]
			for component in self.dict_comp:
				if self.dict_comp[component].weight <= self.dict_launch[node.depth + 1].max_payload:
					state = [component]
					path_cost = node.path_cost + self.dict_launch[node.depth+1].var_cost * self.dict_comp[component].weight
					new_virtual_nodes.append(Node(parent = node, state = state, depth = node.depth + 1, 
													path_cost = path_cost, payload = self.dict_comp[component].weight))

		# other case loop through all received nodes
		else:
			for node in nodes:
				possible_components = []
				# collect neighbours of every component in space
				for component in node.state:
					neighbours = self.dict_comp[component].list_adj
					# verify if the neighbours are already in space or were already added to the list of possible components to lauch
					for neighbour in neighbours:
						if not (neighbour in node.state) or (neighbour in possible_components):
							possible_components.append(neighbour)
							
				for component in possible_components:
					possible_state = list(node.state)
					possible_state.append(component)
					# check if created state already exists
					if not self.CheckRepeatedlStates(possible_state, virtual_states):
						# add state to list of current reached states
						virtual_states.append(possible_state)
						
						# if node is the parent payload we dont had past payload
						if node == parent:
							payload = self.dict_comp[component].weight
						else:
							payload = self.dict_comp[component].weight + node.payload
						
						if payload <= self.dict_launch[parent.depth + 1].max_payload:
							path_cost = node.path_cost + self.dict_launch[parent.depth+1].var_cost * self.dict_comp[component].weight
							new_virtual_nodes.append(Node(parent = parent, state = possible_state, depth = parent.depth+1, 
															path_cost = path_cost, payload = payload))
		return new_virtual_nodes			

	def PathCostFunc(self, node, parent):
		'Function that calculates path cost'
		return node.path_cost + self.dict_launch[node.depth].fixed_cost
	
	def EvaluationFunc(self, node, parent):
		'Evaluation Function of current node f = g + h'
		f = self.PathCostFunc(node,parent)
		node.heuristic = self.Heuristic5(node)
		return (f + node.heuristic - parent.heuristic)
	
	def Heuristic1(self, node):
		'Heuristic 1'	

		# left components missing in space
		left_states = set(self.dict_comp.keys()) - set(node.state)	
		total_weight = 0
		
		# total weight from left components
		for state in left_states:
			total_weight = total_weight + self.dict_comp[state].weight 
		
		# list of costs considering total weight for every left launch 
		if total_weight !=0:
			lista = [self.dict_launch[x+1].fixed_cost + total_weight * self.dict_launch[x+1].var_cost
					for x in range(node.depth,len(self.dict_launch))] 
			if lista == []:
				return 0
			# heuristic chooses the min of the cost 
			return min(lista)
		return 0

	def Heuristic2(self,node):
		'Heuristic 2 it is based in heuristic 1 but considers the cost density of the launches'
		left_states = set(self.dict_comp.keys()) - set(node.state)	
		total_weight = 0
		
		for state in left_states:
			total_weight = total_weight + self.dict_comp[state].weight 
		
		if(total_weight !=0):
			lista = [self.dict_launch[x+1].cost_density*total_weight
					for x in range(node.depth,len(self.dict_launch))] 
		
			if lista == []:
				return 0
			return min(lista)

		return 0 

	def Heuristic3(self,node):
		'Heuristic 3'
		left_states = set(self.dict_comp.keys()) - set(node.state)	
		total_weight = 0
		heuristic = 0
		
		if node.depth+1 in self.dict_launch:
			for state in left_states:
				total_weight = total_weight + self.dict_comp[state].weight

			lista = sorted([[self.dict_launch[x+1].cost_density,x+1] 
							for x in range(node.depth,len(self.dict_launch))],
							key = lambda t: t[0])
		
			while total_weight != 0:
				for launch in lista:			
					if self.dict_launch[launch[1]].max_payload < total_weight :
						total_weight = total_weight - self.dict_launch[launch[1]].max_payload;
						heuristic = self.dict_launch[launch[1]].cost_density*self.dict_launch[launch[1]].max_payload;
					else:
						heuristic = heuristic + self.dict_launch[launch[1]].cost_density*total_weight
						total_weight = 0
						break

		return heuristic

	def Heuristic4(self,node):
		left_states = set(self.dict_comp.keys()) - set(node.state)	
		total_weight = 0
		heuristic = 0
		
		if node.depth+1 in self.dict_launch:
			for state in left_states:
				total_weight = total_weight + self.dict_comp[state].weight

			lista = sorted([[self.dict_launch[x+1].cost_density,x+1] for x in range(node.depth,len(self.dict_launch))] , key=lambda t: t[0])
		
			while total_weight != 0:
				for i in range(len(lista)):
					launch = lista[i]			
					if self.dict_launch[launch[1]].max_payload < total_weight :
						total_weight = total_weight - self.dict_launch[launch[1]].max_payload;
						heuristic = self.dict_launch[launch[1]].cost_density*self.dict_launch[launch[1]].max_payload;
					else:
						extra_cost = [self.dict_launch[lista[j][1]].fixed_cost+self.dict_launch[lista[j][1]].var_cost*total_weight for j in range(i,len(lista))]
						#print(self.dict_launch[launch[1]].cost_density*total_weight,min(extra_cost),extra_cost.index(min(extra_cost)),i)
						heuristic = heuristic + min(extra_cost)
						total_weight = 0
						break

		return heuristic

	def Heuristic5(self, node):
		lista = [self.Heuristic1(node), self.Heuristic2(node), self.Heuristic3(node)]
		return max(lista)

	def CheckRepeatedlStates(self, list1, list_lists):
		'Check repeated list in a list of list'
		for l in list_lists:
			if set(list1) == set(l):
				return True 
		return False

	def CheckPossiblePayload(self,node):
		'Check if there is enough payload in the left launches '
		left_states = set(self.dict_comp.keys()) - set(node.state)	
		weight_missing = 0
		weight_possible = 0
		
		for state in left_states:
			weight_missing = weight_missing + self.dict_comp[state].weight 

		for i in range(node.depth,len(self.dict_launch)):
			weight_possible = weight_possible + self.dict_launch[i+1].max_payload

		if weight_missing <= weight_possible:
			return True
		else:
			return False

	def PrintEffectiveBF(self):
		print("Ngen = " + str(self.nodes_generated))
		print("Nexp = " + str(self.n_expanded))
		print("d = " + str(self.final_depth))
		print("b = " + str(exp(log1p(self.nodes_generated)/self.final_depth)))

class Node(object):

	def __init__(self, parent = None, state = [], depth = 0, path_cost = 0, payload = 0):
		self.parent = parent
		# list with name of components already in space
		self.state = state
		# cost of all movements until this node
		self.path_cost = path_cost
		# max is number of launches
		self.depth = depth
		# payload in this launch
		self.payload = payload
		# value of heuristic
		self.heuristic = 0

	def __repr__(self):
		return " state = " + str(self.state) + " path_cost = " + str(self.path_cost) + ' d = ' + str(self.depth) +  " h = " + str(self.heuristic)

	def __lt__(self,other):
		return self.path_cost < other.path_cost

	def __eq__(self,other):
		if self.depth != other.depth:
			return False
		if set(self.state) == set(other.state):
			return True
		return False
		