import numpy as np
import gym
import gym_minigrid
import pickle
import matplotlib
import matplotlib.pyplot as plt
import imageio
import sys

from Node import *

MF = 0 # Move Forward (MF)
TL = 1 # Turn Left (TL)
TR = 2 # Turn Right (TR)
PK = 3 # Pickup Key (PK)
UD = 4 # Unlock Door (UD)

def step_cost(action):
    '''
    We only have a positive cost for movement forward. Turning and interacting
    with objects in the maze does not cost anything.
    '''
    if action == MF:
        return 1
    else:
        return 0

def step(env, action):
    '''
    Take Action
    ----------------------------------
    actions:
        0 # Move forward (MF)
        1 # Turn left (TL)
        2 # Turn right (TR)
        3 # Pickup the key (PK)
        4 # Unlock the door (UD)
    '''
    actions = {
        0: env.actions.forward,
        1: env.actions.left,
        2: env.actions.right,
        3: env.actions.pickup,
        4: env.actions.toggle
    }

    _, _, done, _ = env.step(actions[action])
    return step_cost(action), done

def generate_random_env(seed, task):
    '''
    Generate a random environment for testing
    -----------------------------------------
    seed:
        A Positive Integer,
        the same seed always produces the same environment
    task:
        'MiniGrid-DoorKey-5x5-v0'
        'MiniGrid-DoorKey-6x6-v0'
        'MiniGrid-DoorKey-8x8-v0'
    '''
    if seed < 0:
        seed = np.random.randint(50)
    env = gym.make(task)
    env.seed(seed)
    env.reset()
    return env

def load_env(path):
    '''
    Load Environments
    ---------------------------------------------
    Returns:
        env (gym-environment), info, g (graph)
    '''

    with open(path, 'rb') as f:
        env = pickle.load(f)

    info = {
        'height': env.height,
        'width': env.width,
        'init_agent_pos': env.agent_pos,
        'init_agent_dir': env.dir_vec
    }

    info['wall_pos'] = []

    graph = [([None] * info['width']) for row in range(info['height'])] # initialize graph

    for i in range(env.height):
        for j in range(env.width):
            if isinstance(env.grid.get(j, i), gym_minigrid.minigrid.Wall):
                # leave these as None in graph
                # info['wall_pos'].append((j, i))
                continue

            elif isinstance(env.grid.get(j, i), gym_minigrid.minigrid.Key):
                info['key_pos'] = np.array([j, i])
                keyNode = Node(j, i)
                keyNode.setKey(True)
                graph[j][i] = keyNode

            elif isinstance(env.grid.get(j, i), gym_minigrid.minigrid.Door):
                info['door_pos'] = np.array([j, i])
                doorNode = Node(j, i)
                doorNode.setDoor(True)
                doorNode.setLock(False)
                graph[j][i] = doorNode

            elif isinstance(env.grid.get(j, i), gym_minigrid.minigrid.Goal):
                info['goal_pos'] = np.array([j, i])
                goalNode = Node(j, i)
                goalNode.setGoal(True)
                graph[j][i] = goalNode

            else:
                n = Node(j, i)
                graph[j][i] = n

    graph[info['init_agent_pos'][0]][info['init_agent_pos'][1]].setStart(True)

    return env, info, graph

def save_env(env, path):
    with open(path, 'wb') as f:
        pickle.dump(env, f)

def plot_env(env):
    '''
    Plot current environment
    ----------------------------------
    '''
    img = env.render('rgb_array', tile_size=50)
    plt.figure()
    plt.imshow(img)
    plt.show()

def draw_gif_from_seq(seq, env, path='./gif/doorkey.gif'):
    '''
    Save gif with a given action sequence
    ----------------------------------------
    seq:
        Action sequence, e.g [0, 0, 0, 0] or [MF, MF, MF, MF]

    env:
        The doorkey environment
    '''

    path = './gif/' + path + '.gif'
    with imageio.get_writer(path, mode='I', duration=0.8) as writer:
        img = env.render('rgb_array', tile_size=50)
        writer.append_data(img)
        for act in seq:
            step(env, act)
            img = env.render('rgb_array', tile_size=50)
            writer.append_data(img)
    print('Maze traversal GIF is written to {}'.format(path))
    return

def draw_value_iteration(optVal, path='./vals/valueIteration'):
    #opt = np.concatenate((optVal1, optVal2), axis=2)

    path = './vals/' + path
    for f in range(optVal.shape[2]):
        optVal[:, :, f][optVal[:, :, f] > 255] = 255
        frame = optVal[:, :, f].astype(np.uint8)

        fig, ax = plt.subplots()
        im = ax.imshow(frame)
        title = "value iteration: " + path[7:] + str(f)

        xlabels = [str(i) for i in range(optVal.shape[0])]
        ylabels = [str(j) for j in range(optVal.shape[1])]

        ax.set_xticks(np.arange(len(xlabels)))
        ax.set_yticks(np.arange(len(ylabels)))

        ax.set_xticklabels(xlabels)
        ax.set_yticklabels(ylabels)

        plt.setp(ax.get_xticklabels(), rotation=0, ha="right", rotation_mode="anchor")

        for i in range(len(ylabels)):
            for j in range(len(xlabels)):
                text = ax.text(j, i, frame[i, j], ha="center", va="center", color="w")

        ax.set_title(title)
        fig.tight_layout()
        fig.savefig(path + str(f), dpi=300)
        plt.show()

    return

def plot_special_state_values(graph, optVal, specialNode, path='./cells/valuesVsTime'):
    '''
    Plot the values of all valid cells around a given special cell, e.g. a Key, Door, or Goal
    '''
    path = './cells/' + path
    optVal[:, :, :][optVal[:, :, :] > 255] = 255
    children = []

    # Add all surrounding states that we are interested in
    if (graph[specialNode[0]][specialNode[1]].has_door):
        children.append(graph[specialNode[0] - 1][specialNode[1]]) # only interested in cell to left of Door
    else:
        children.append(graph[specialNode[0] - 1][specialNode[1]])
        children.append(graph[specialNode[0] + 1][specialNode[1]])
        children.append(graph[specialNode[0]][specialNode[1] - 1])
        children.append(graph[specialNode[0]][specialNode[1] + 1])

    validChildren = list(filter(None, children)) # filter out Walls from successor nodes

    for child in validChildren:
        title = path[8:] + ", value vs iterations: " + str(child)
        time = np.arange(optVal.shape[2])
        values = optVal[child.i, child.j, :]

        plt.plot(time, values)
        plt.grid()

        plt.title(title)
        plt.savefig(path + "-" + str(child) + ".png", dpi=300, bbox_inches='tight')
        plt.show()
    return

def action_sequence_to_string(actSeq):
    dictionary = {
        MF : "MF", # Move Forward (MF)
        TL : "TL", # Turn Left (TL)
        TR : "TR", # Turn Right (TR)
        PK : "PK", # Pickup Key (PK)
        UD : "UD", # Unlock Door (UD)
    }

    return ", ".join([dictionary[a] for a in actSeq])

