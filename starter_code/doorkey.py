import numpy as np
import gym
import glob
import matplotlib.pyplot as plt
import sys

from utils import *
from Node import *
from PriorityQueue import *

PLOTTING = False

MF = 0 # Move Forward (MF)
TL = 1 # Turn Left (TL)
TR = 2 # Turn Right (TR)
PK = 3 # Pickup Key (PK)
UD = 4 # Unlock Door (UD)

def resetNodes(graph, beginNode, endNode):
    '''
    The LCA requires labels and transition costs of the Nodes of the graph to
    obey certain conditions.
    Given a graph and coordinates (tuples) of the initial Node and target Node,
    we set the labels appropriately.
    Make sure to extract the optimal values and the parent sequence before this.
    '''
    t = 0 # since we always run this before beginning the search

    for i in range(len(graph[1])):
        for j in range(len(graph[0])):
            if graph[j][i] is not None:
                graph[j][i].resetNode()

    graph[beginNode[0]][beginNode[1]].correctLabel(t, 0)
    graph[endNode[0]][endNode[1]].stage_cost = 0

def getOptimalValues(graph, T):
    '''
    Given a graph of Nodes that has been searched, extract the values over every timestep <= T
    '''
    opt = sys.maxsize * np.ones((len(graph[1]), len(graph[0]), T + 1))

    for i in range(len(graph[0])):
        for j in range(len(graph[1])):
            if graph[j][i] is not None:
                opt[i, j, np.array(list(graph[j][i].values.keys()))] = np.array(list(graph[j][i].values.values()))

    for k in range(T):
        opt[:, :, k + 1] = np.minimum(opt[:, :, k], opt[:, :, k + 1])

    return opt

def getNodeSequence(graph, beginNode, endNode):
    '''
    Given a graph of Nodes, returns the forward sequence of nodes (from beginNode to endNode)

    '''
    n = graph[endNode[0]][endNode[1]]
    parents = [] # backward sequence

    while n is not None:
        parents.append(n)
        n = n.parent

    nodeSeq = list(reversed(parents)) # forward sequence
    return nodeSeq

def getActionSequence(graph, nodeSeq, init_orientation):
    '''
    Given a graph of Nodes and the path the agent travels, returns the action sequence of the agent (from beginNode to endNode)

    actions:
        0 # Move forward (MF)
        1 # Turn left (TL)
        2 # Turn right (TR)
        3 # Pickup the key (PK)
        4 # Unlock the door (UD)
    '''
    actSeq = []
    turns = {
        # given (currOrientation, nextOrientation) output corresponding turn action
        ((-1, 0), (0, 1))  : TL,
        ((-1, 0), (0, -1)) : TR,

        ((1, 0), (0, 1))   : TR,
        ((1, 0), (0, -1))  : TL,

        ((0, -1), (-1, 0)) : TL,
        ((0, -1), (1, 0))  : TR,

        ((0, 1), (-1, 0))  : TR,
        ((0, 1), (1, 0))   : TL
    }

    for n in range(len(nodeSeq) - 1):

        # handle orientations and single forward movement
        currNode = nodeSeq[n]
        nextNode = nodeSeq[n + 1]

        if (n == 0):
            currOrientation = (init_orientation[0], init_orientation[1])
        else:
            currOrientation = nextOrientation

        nextOrientation = (nextNode.j - currNode.j, nextNode.i - currNode.i)

        # Turning actions
        if (nextOrientation == (-1 * currOrientation[0], -1 * currOrientation[1])): # U-turn
            actSeq.append(TL)
            actSeq.append(TL)
        elif (nextOrientation != currOrientation): # 90-degree turns
            actSeq.append(turns[(currOrientation, nextOrientation)])

        # Special actions
        if nextNode.has_key:
            actSeq.append(PK)
            nextNode.setKey(False)
            #continue
        if nextNode.has_door and not nextNode.door_unlocked:
            actSeq.append(UD)
            # actSeq.append(MF)
            nextNode.setLock(True)

        # Forward movement
        if not nextNode.has_key:
            actSeq.append(MF)

    return actSeq, nextOrientation

def getChildren(graph, j, i):
    '''
    Obtains the possible successors from a Node at position (j, i) in a graph

    '''
    children = []

    # All possible actions
    children.append(graph[j+1][i])
    children.append(graph[j][i+1])
    children.append(graph[j-1][i])
    children.append(graph[j][i-1])

    validChildren = list(filter(None, children)) # filter out Walls from successor nodes
    return validChildren

def labelCorrectingAlgorithm(graph, beginNode, endNode):
    '''
    Perform the LCA given a graph (2D list of Nodes), and coordinates (tuples) of the initial Node and target Node

    '''
    # initialize time count
    t = 0
    resetNodes(graph, beginNode, endNode)

    EXPLORED = set()

    OPEN = PriorityQueue()

    OPEN.push(graph[beginNode[0]][beginNode[1]]) # add beginNode to OPEN frontier
    EXPLORED.add(graph[beginNode[0]][beginNode[1]]) # add beginNode to set of EXPLORED nodes

    # labels were initialized in the Node class

    found = False
    while not OPEN.isEmpty() and not found:
        t += 1

        parent = OPEN.pop()

        children = getChildren(graph, parent.j, parent.i)

        for child in children:
            if (parent.label + child.stage_cost) < child.label and (parent.label + child.stage_cost) < graph[endNode[0]][endNode[1]].label:
                child.correctLabel(t, parent.label + child.stage_cost)
                child.setParent(parent)

                EXPLORED.add(child)
                if child != graph[endNode[0]][endNode[1]]:
                    OPEN.push(child)
                else:
                    found = True
                    break

    return EXPLORED, t

if __name__ == '__main__':
    env_paths = glob.glob('.\\envs\\*.env')

    for i in range(len(env_paths)):
        env_path = env_paths[i]
        print()
        print(env_path[7:-4])

        env, info, graph = load_env(env_path) # load an environment

        ########### OBTAIN SEQUENCE FROM EITHER EXPLORED OR FROM OPT #############

        print()
        FIRST, T1 = labelCorrectingAlgorithm(graph, info['init_agent_pos'], info['key_pos']) # set of explored nodes
        FIRST = dict(zip([str(n.getCoords()) for n in FIRST], [n.label for n in FIRST]))

        opt1 = getOptimalValues(graph, T1)
        nodeSeq1 = getNodeSequence(graph, info['init_agent_pos'], info['key_pos'])
        print("shortest node sequence: START to KEY")
        print([n.getCoords() for n in nodeSeq1])
        print()

        SECOND, T2 = labelCorrectingAlgorithm(graph, info['key_pos'], info['goal_pos'])
        SECOND = dict(zip([str(n.getCoords()) for n in SECOND], [n.label for n in SECOND]))

        opt2 = getOptimalValues(graph, T2)
        nodeSeq2 = getNodeSequence(graph, info['key_pos'], info['goal_pos'])
        print("shortest node sequence: KEY to GOAL")
        print([n.getCoords() for n in nodeSeq2])
        print()

        if PLOTTING:
            # Output value iteration
            draw_value_iteration(opt1, env_path[7:-4] + "-StartToKey, t = ")
            draw_value_iteration(opt2, env_path[7:-4] + "-KeyToGoal, t = ")

            # Plot value vs iteration curves for selected states
            plot_special_state_values(graph, opt1, info['key_pos'], env_path[7:-4] + "-StartToKey")
            plot_special_state_values(graph, opt1, info['door_pos'], env_path[7:-4] + "-StartToKey")
            plot_special_state_values(graph, opt1, info['goal_pos'], env_path[7:-4] + "-StartToKey")

            plot_special_state_values(graph, opt2, info['key_pos'], env_path[7:-4] + "-KeyToGoal")
            plot_special_state_values(graph, opt2, info['door_pos'], env_path[7:-4] + "-KeyToGoal")
            plot_special_state_values(graph, opt2, info['goal_pos'], env_path[7:-4] + "-KeyToGoal")

        actSeq1, intermediateOrientation = getActionSequence(graph, nodeSeq1, info['init_agent_dir'])
        print("action sequence: START to KEY")
        print(actSeq1)
        print()

        actSeq2, finalOrientation = getActionSequence(graph, nodeSeq2, intermediateOrientation)
        print("action sequence: KEY to GOAL")
        print(actSeq2)
        print()

        nodeSeq = nodeSeq1 + nodeSeq2
        print("complete shortest node sequence: START to GOAL")
        print(" to ".join([str(n) for n in nodeSeq]))
        print()

        actSeq = actSeq1 + actSeq2
        print("complete action sequence: START to GOAL")
        print(actSeq)
        print(action_sequence_to_string(actSeq))
        print()

        draw_gif_from_seq(actSeq, load_env(env_path)[0], env_path[7:-4]) # draw a GIF & save
        print()