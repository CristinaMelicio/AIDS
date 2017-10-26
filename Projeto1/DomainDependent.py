import datetime
import sys

class Component(object):

	def __init__(self, vID = None, weight = 0):
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
		self.dateID = dateID
		self.max_payload = max_payload
		self.fixed_cost = fixed_cost
		self.var_cost = var_cost
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
		# mode uniformed / informed
		self.mode = mode	
		# dictionary of components
		self.dict_comp = {}
		# dicionary of launches (ordered by date, key goes from 1 to number of launches)
		self.dict_launch = {}
		# number generated nodes
		self.n_nodes = 0
		# decisions to be made
		self.decisions = []
		# total cost
		self.final_cost = 0
		# initial state
		self.initial_state = Node()		
		
		if mode == '-u':
			self.func = self.FPathCost
		elif mode == '-i':
			self.func = self.FPathCostHeur

		try:
			file = open(file, "r")
		except IOError:
			print ("ERROR: There is not such a file")
			exit()

		for line in file:
			if line[0] == 'V':
				line = line.strip('\n')
				comp_id = line.split(None, 1)[0]
				comp_w  = float(line.split(None, 1)[1])			
				try: 
					self.dict_comp[comp_id].SetWeight(comp_w)
				except:
					self.dict_comp[comp_id] = Component(comp_id, comp_w)
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

		
	# checks if all elements are in space
	def GoalTest(self, node):
		if set(node.state) == set(self.dict_comp.keys()):
			self.final_cost = node.path_cost
			return True
		else:
			return False

	# traces all decisions made until the initial node
	def Traceback(self, node):
		while not (node.state == []):
			dif_components = set(node.state) - set(node.parent.state)
			dif_costs = node.path_cost-node.parent.path_cost - node.heuristic + node.parent.heuristic
			if node.payload != 0:
				self.decisions.append(self.dict_launch[node.depth].dateID.strftime('%d%m%Y') 
									+ ' ' + ' '.join(dif_components) + ' ' + str(dif_costs))
			node = node.parent

	# Print All Decisions from the initial state to goal state
	def PrintDecisions(self):
		s = ""
		for i in range(len(self.decisions)):
			s += str(self.decisions[-(i+1)]) + "\n"
		s += ("%.10f")%self.final_cost
		return s

	# SucessorFunction
	def Successor(self, node):
		# all nodes derived from the recursive expansion
		new_nodes = []
		# not expand last node
		if (node.depth + 1) in self.dict_launch:
			# nodes generated in each recursive call of expansion
			virtual_nodes = [node]
			
			while virtual_nodes:
				virtual_nodes = self.Expand(virtual_nodes, node)
				for virtual_node in virtual_nodes:
					new_nodes.append(virtual_node)
			
			for new_node in new_nodes:
				new_node.path_cost = self.func(new_node, node)
			#add empty launch
			new_nodes.append(Node(parent = node, state = node.state, 
										path_cost = node.path_cost, 
										depth = node.depth+1))	

		return new_nodes

	def Expand(self, nodes, parent):
		# auxiliary to store already generated states (used for comparsion)
		virtual_states = []
		# stores all new nodes
		new_virtual_nodes = []


		# Case of one empty node case
		if nodes[0].state == []:
			#print('case []')
			node = nodes[0]
			for component in self.dict_comp:
				if self.dict_comp[component].weight <= self.dict_launch[node.depth + 1].max_payload:
					state = [component]
					#path_cost = self.func(node) 
					path_cost = node.path_cost + self.dict_launch[node.depth+1].var_cost * self.dict_comp[component].weight
					new_virtual_nodes.append(Node(parent = node, state = state, depth = node.depth + 1, 
													path_cost = path_cost, payload = self.dict_comp[component].weight))

		# other case loop trough all received nodes
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
						if (payload <= self.dict_launch[parent.depth + 1].max_payload):
							path_cost = node.path_cost + self.dict_launch[parent.depth+1].var_cost * self.dict_comp[component].weight
							new_virtual_nodes.append(Node(parent = parent, state = possible_state, depth = parent.depth+1, 
															path_cost = path_cost, payload = payload))

		return new_virtual_nodes			

	def FPathCost(self, node, parent):
		return node.path_cost + self.dict_launch[node.depth].fixed_cost
	
	def FPathCostHeur(self, node, parent):
		f = self.FPathCost(node,parent)
		node.heuristic = self.Heuristic2(node)
		#print(node)
		return (f + node.heuristic - parent.heuristic)
	
	def Heuristic1(self, node):	
		left_states = set(self.dict_comp.keys()) - set(node.state)	
		total_weight = 0
		
		for state in left_states:
			total_weight = total_weight + self.dict_comp[state].weight 
		
		lista = [self.dict_launch[x].fixed_cost + total_weight * self.dict_launch[x].var_cost
					for x in range(node.depth,len(self.dict_launch))] 
		
		if lista == []:
			return 0
		return min(lista)


	def Heuristic2(self,node):
		left_states = set(self.dict_comp.keys()) - set(node.state)	
		total_weight = 0
		heuristic = 0
		#print(node)
		
		if node.depth+1 in self.dict_launch:
			for state in left_states:
				total_weight = total_weight + self.dict_comp[state].weight

			lista = sorted([[self.dict_launch[x].cost_density,x] for x in range(node.depth,len(self.dict_launch))] , key=lambda t: t[0])
			#print(lista)

		
			while total_weight != 0:
				for launch in lista:
					# print(launch)
					# print(self.dict_launch[launch[1]].max_payload)			
					if self.dict_launch[launch[1]].max_payload < total_weight :
						total_weight = total_weight - self.dict_launch[launch[1]].max_payload;
						heuristic = self.dict_launch[launch[1]].cost_density*self.dict_launch[launch[1]].max_payload;
						#print('h1',heuristic)
					else:
						heuristic = heuristic + self.dict_launch[launch[1]].cost_density*total_weight
						total_weight = 0
						#print('h2',heuristic)
						break
		#print(heuristic)

		return heuristic


	def CheckRepeatedlStates(self, list1, list_lists):
		for l in list_lists:
			if set(list1) == set(l):
				return True 
		return False

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
		# 
		self.heuristic = 0
		#

	def __repr__(self):
		return " state = " + str(self.state) + " path_cost = " + str(self.path_cost) + ' d = ' + str(self.depth) +  "h = " + str(self.heuristic)


	def __lt__(self,other):
		return self.path_cost < other.path_cost

	def __eq__(self,other):
		if self.depth != other.depth:
			return False
		if set(self.state) == set(other.state):
			return True
		return False
		