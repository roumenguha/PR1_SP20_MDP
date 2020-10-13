#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on Tue Apr 21 22:21:43 2020

@author: roume

Adapted from https://www.geeksforgeeks.org/priority-queue-in-python/
"""

from Node import *
from operator import attrgetter

# A simple implementation of Priority Queue using lists in Python.

class PriorityQueue(object):

    def __init__(self):
        self.queue = []

    def __str__(self):
        result = sorted(self.queue, key=attrgetter('label'))
        return ' '.join([str(i) for i in result])

    def __len__(self):
        return len(self.queue)

    def isEmpty(self):
        return len(self.queue) == 0

    # for inserting an element in the queue

    def push(self, n):
        self.queue.append(n)
        return

    # for popping a node based on priority

    def pop(self):
        try:
            min_index = 0
            for i in range(len(self.queue)):
                if self.queue[i].label < self.queue[min_index].label:
                    min_index = i
            item = self.queue[min_index]
            del self.queue[min_index]
            return item
        except IndexError:
            print ()
            exit()


if __name__ == '__main__':
    myQueue = PriorityQueue()

# ....myQueue.push(12)
# ....myQueue.push(1)
# ....myQueue.push(14)
# ....myQueue.push(7)
# ....print(myQueue)
# ....while not myQueue.isEmpty():
# ........print(myQueue.pop())

