import datetime

class Component:

	def __init__(self, ID = None, weight = 0):
		self.ID = ID 
		self.weight = weight
		self.list_adj = []

	def SetAdjacents(self, IDadj):
		self.list_adj.append(IDadj)

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
	
	def __init__(self, IDdate = None, max_weight = 0, var_cost = 0):
		self.IDdate = IDdate
		self.max_weight = max_weight
		self.var_cost = var_cost



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
				date = line.split()[1]
				try:
					print(datetime.datetime.strptime(date, '%d%m%Y').date())
				except:
					print("Error")

		file.close()

	def getDictComponents(self):
		return self.dict_comp

