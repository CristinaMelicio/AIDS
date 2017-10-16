class Component:

	def __init__(self, ID = None, weight=0):
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
		return ID

	def GetWeight(self):
		return weight

	def GetListAdj(self):
		return list_adj

class Graph(Component):

	def __init__(self, file):
		self.dict_comp = {}

		file = open(file, "r")

		for line in file:
			if line[0] == 'V':
				line = line.strip('\n')		
				comp_id = line.split(None, 1)[0]
				comp_w  = line.split(None, 1)[1]
				
				try: 
					self.dict_comp[comp_id].SetWeight(w)
				except:
					self.dict_comp[comp_id] = Component(comp_id, comp_w)
					self.dict_comp[comp_id].SetWeight(comp_w)

			elif line[0] == 'E':
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

		file.close()

	def getDictComponents(self):
		return self.dict_comp

