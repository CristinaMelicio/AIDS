import datetime
from collections import OrderedDict

class Component:

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

	def GetID(self):
		return self.ID

	def GetWeight(self):
		return self.weight

	def GetListAdj(self):
		return self.list_adj

class Launch:
	
	def __init__(self, dateID = None, max_payload = 0, fixed_cost = 0, var_cost = 0):
		self.dateID = dateID
		self.max_payload = max_payload
		self.fixed_cost = fixed_cost
		self.var_cost = var_cost

	def SetIDdate(self, dateID):
		self.dateID = dateID

	def SetMaxPayload(self, max_payload):
		self.max_payload = max_payload

	def SetFixedCost(self, fixed_cost):
		self.fixed_cost = fixed_cost

	def SetVarCost(self, var_cost):
		self.var_cost = var_cost

	def __repr__(self):
		return str(self.max_payload) + "," +  str(self.fixed_cost) + "," +  str(self.var_cost) + "\n" 	

# adicionei float() em sitios para poder fazer contas com os valores
# apaguei uma linha numa das condicoes que nao era preciso
# adicionei n_nodes para sabermos quantos nos foram gerados
# arranjei maneira de ordenar o dicionario
class Graph(Component, Launch):

	def __init__(self, file):
		self.dict_comp = {}
		self.dict_launch = {}
		# number generated nodes
		self.n_nodes = 0

		file = open(file, "r")

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


	def GetDictComponents(self):
		return self.dict_comp

	def GetDictLaunchs(self):
		self.dict_launch = dict(OrderedDict(sorted(self.dict_launch.items(), key=lambda t: t[0])))
		return self.dict_launch


class Node:

	def __init__(self, parent = None, state = [], depth = 0, path_cost = 0, payload = 0, n_launch = 0):
		self.parent = parent
		# list with name of components already in space
		self.state = state
		# cost of all movements until this node
		self.path_cost = path_cost
		# max is number of launches
		self.depth = depth
		# payload in this launch
		self.payload = payload
		# for now useless, check in the end to clean if needed
		self.n_launch = n_launch

	# def __repr__(self):
	# 	return " state = " + str(self.state) + " path_cost = " + str(self.path_cost) + ' d = ' + str(self.depth) + "\n"

	def print_info(self):
		print (" state = ", self.state, " path_cost = ", self.path_cost,' d = ', self.depth, "payload = ", self.payload, "parent =" , self.parent,)
