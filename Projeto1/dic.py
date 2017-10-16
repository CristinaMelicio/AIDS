file = open("mir.txt", "r")


weights_dict = {}
edges_dict = {}
edge1 = []
edge2 = []

for line in file:
	if line[0] == 'V':
		line = line.strip('\n')
		v = line.split(None, 1)[0]
		w = line.split(None, 1)[1]
		weights_dict[v] = w
		
	elif line[0] == 'E':
		edge1.append(line.split()[1])
		edge2.append(line.split()[2])

for i in range(len(edge1)):
	try:
		edges_dict[edge1[i]] = edges_dict[edge1[i]] , edge2[i]
	except KeyError:
		edges_dict[edge1[i]] = edge2[i]
for i in range(len(edge2)):
	try:
		edges_dict[edge2[i]] = edges_dict[edge2[i]] , edge1[i]
	except KeyError:
		edges_dict[edge2[i]] = edge1[i]

#components_dict[weights_dict] = {}
#components_dict['components']['edges'] = weights_dict.values()
#components_dict['components']['weights'] = 

ds = [weights_dict, edges_dict]
d = {}
for k in weights_dict.keys():
    d[k] = tuple(d[k] for d in ds)

print(d)

file.close()
