# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 19:10:55 2020

@author: roume
"""

'''
Purpose: This class represents any cell of the maze that is traversable (i.e. are not wall/river)
'''

import sys

class Node(object):
    MAX_LABEL = sys.maxsize

    MAX_STAGE_COST = 1 # transition cost
    GOAL_REWARD = 0 #


    def __init__(self, j: int, i: int):
        self.j = j
        self.i = i
        self.is_start = False
        self.is_goal = False
        self.has_key = False
        self.has_door = False
        self.door_unlocked = False

        self.label = Node.MAX_LABEL
        self.stage_cost = Node.MAX_STAGE_COST # - 20 * has_key - 100 * is_goal

        self.values = {
            0: self.label
        } # where we store the labels (values) over iterations t

        self.parent = None

    def __str__(self):
        return str((self.j, self.i))

    def setStart(self, is_start: bool):
        self.is_start = is_start

    def setGoal(self, is_goal: bool):
        self.is_goal = is_goal

    def setKey(self, has_key: bool):
        self.has_key = has_key

    def setDoor(self, has_door: bool):
        self.has_door = has_door

    def setLock(self, door_unlocked: bool):
        self.door_unlocked = door_unlocked

    def setParent(self, parent):
        self.parent = parent

    def getCoords(self):
        return (self.j, self.i)

    def correctLabel(self, t, newLabel):
        self.values[t] = newLabel

        self.label = newLabel

    def resetNode(self):
        self.correctLabel(0, Node.MAX_LABEL)
        self.stage_cost = Node.MAX_STAGE_COST

        self.values = {
            0: self.label
        }

        self.parent = None