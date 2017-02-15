# 
# A naive implementation of Graph Edit Distance with node edit operations only
# (including add a node, remove a node, and substitute a node) 
# 
# Reference: "Bridge the Gap Between Graph Edit Distance and Kernel Machines"
#  
# Author: Zhongjun Jin
# 

# Calculate the cost of edit path
def cost_edit_path(edit_path):
	cost = 0
	new_path = []

	for operation in edit_path:
		
		# Vertex substitution
		if operation[0] and operation[1]:
			cost += 1

		# Remove vertex u
		elif operation[0]:
			cost += 1

		# Add vertex v
		else:
			cost += 1

	return cost

# Check unprocessed nodes in graph u and v
def check_unprocessed(u,v,path):
	processed_u = []
	processed_v = []

	for operation in path:
		if operation[0]:
			processed_u.append(operation[0])

		if operation[1]:
			processed_v.append(operation[1])

	unprocessed_u = u.nodes_set() - set(processed_u)
	unprocessed_v = v.nodes_set() - set(processed_v)
	return  list(unprocessed_u),list(unprocessed_v)




def graph_edit_distance(u,v):

	# Partial edit path
	open_set = []
	cost_open_set = []


	# For each node w in V2, insert the substitution {u1 -> w} into OPEN
	u1 = u.nodes()[0]
	
	for w in v.nodes():
		edit_path = set()
		edit_path.add((u1,w))

		new_cost = cost_edit_path(edit_path)

		open_set.append(edit_path)
		cost_open_set.append(new_cost)


	# Insert the deletion {u1 -> none} into OPEN
	edit_path = set()
	edit_path.add((u1,None))
	new_cost = cost_edit_path(edit_path)

	open_set.append(edit_path)
	cost_open_set.append(new_cost)


	while cost_open_set:
		# Retrieve minimum-cost partial edit path pmin from OPEN
		path_idx = cost_open_set.index(min(cost_open_set))
		min_path = open_set.pop(path_idx)
		cost = cost_open_set.pop(path_idx)

		# Check p_min is a complete edit path
		unprocessed_u,unprocessed_v = check_unprocessed(u,v,min_path)

		# Return if p_min is a complete edit path
		if not unprocessed_u and not unprocessed_v:
			return min_path,cost

		else:
			if unprocessed_u:
				u_next = unprocessed_u.pop()

				
				for v_next in unprocessed_v:
					new_path = set(min_path)
					new_path.add((u_next,v_next))
					new_cost = cost_edit_path(new_path)
					open_set.append(new_path)
					cost_open_set.append(new_cost)

				new_path = set(min_path)
				new_path.add((u_next,None))
				new_cost = cost_edit_path(new_path)


				open_set.append(new_path)
				cost_open_set.append(new_cost)


			else:
				# All nodes in u have been processed, all nodes in v should be Added.				
				for v_next in unprocessed_v:
					new_path = set(min_path)
					new_path.add((None,v_next))
					new_cost = cost_edit_path(new_path)
					open_set.append(new_path)
					cost_open_set.append(new_cost)

					
	return None,None