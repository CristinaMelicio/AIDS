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
		return "W= " + self.weight + " " + "A= " + str(self.list_adj) + "\n"

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
		return self.max_payload + "," +  self.fixed_cost + "," +  self.var_cost + "\n" 	



class Graph(Component, Launch):

	def __init__(self, file):
		self.dict_comp = {}
		self.dict_launch = {}

		file = open(file, "r")

		for line in file:
			if line[0] == 'V':
				line = line.strip('\n')
				comp_id = line.split(None, 1)[0]
				comp_w  = line.split(None, 1)[1]
				
				try: 
					self.dict_comp[comp_id].SetWeight(comp_w)
				except:
					self.dict_comp[comp_id] = Component(comp_id, comp_w)
					self.dict_comp[comp_id].SetWeight(comp_w)
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
				max_payload = line.split()[2]
				fixed_cost = line.split()[3]
				var_cost = line.split()[4]
				
				self.dict_launch[date_id] = Launch(date_id, max_payload, fixed_cost, var_cost)

		file.close()

	def GetDictComponents(self):
		return self.dict_comp

	def GetDictLaunchs(self):
		self.dict_launch = dict(OrderedDict(sorted(self.dict_launch.items(), key=lambda t: t[0])))
		return self.dict_launch





