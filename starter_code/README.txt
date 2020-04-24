This project is composed of the following files:
	- PriorityQueue.py
	- Node.py
	- utils.py
	- doorkey.py
	
PriorityQueue.py
	- Fairly uninteresting. It's a quick implementation of a priority queue using a list as the underlying data structure, and the label of a Node acting as it's priority value
	- Adapted from https://www.geeksforgeeks.org/priority-queue-in-python/

Node.py
	- Again, a quick Node class. I didn't want to implement a transition matrix because of the complexity in retrieving information from it
	- Each Node instance has a few important properties: 
		+ coordinates: (j, i)
		+ label: scalar value which is reset upon every graph traversal
		+ stage_cost: scalar value which is used to represent the cost of transitioning into this Node
		+ values: dictionary that holds the key-value pair {t: label}. We can extract the label values later for plotting purposes
		+ parent: the Node we set as this Node's parent in the shortest path
		+ some miscellaneous flags, like is_start, is_goal, has_key, has_door, and door_unlocked. They come in handy for some plotting

utils.py
	- Mostly unchanged from the provided utils.py file
	- I edited load_env() to declare and initialize the graph for the project. The graph here is a 2D list of Nodes
	- Added the plotting functions here:
		+ draw_value_iteration(): plots a heat map of the graph nodes' labels over iterations. Since my solution to the problem is to split the goal into two separate label-correcting algorithms (LCAs), I print two heat-map animations for every maze environment
		+ plot_special_state_values(): plots the label costs over iterations for interesting neighbors of a cell in the maze. Intended to be used for Key, Door, and Goal cells
		
doorkey.py
	- This file has been altered heavily from the provided file
	- Contains several functions:
		+ resetNodes(): resets all Nodes in the graph, undoing the work of any previous run of a LCA, allowing any future LCA runs to work correctly
		+ getOptimalValues(): constructs a N x M x T matrix that stores the labels for a node at (n, m) at time t. We make sure to carry the labels from previous timesteps forward
		+ getNodeSequence(): returns a list of Nodes in the order that we traversed them, from startNode to endNode
		+ getActionSequence(): (really annoying to program) returns a list of actions so that we can use the provided draw_gif_from_seq() function
		+ getChildren(): given a node's coordinates (j, i), return the valid neighbor Nodes (non-Wall cells)
		+ labelCorrectingAlgorithm(): Since we implemented the OPEN frontier as a PriorityQueue, this is really just a more specialized version of Dijkstra's algorithm. Returns the set of explored states (that we never ended up using) and T, the total number of iterations used to go grom startNode to endNode
		+ main(): calls all the relevant functions in their correct order