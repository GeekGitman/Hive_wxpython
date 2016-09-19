#!/usr/bin/env python

import sys
sys.path.append('../game/')
from Game import *
import random
import copy
import math

"""
    1.random number generator : randomly(max_number)
    2.map hash : hashmap()
    3.other
"""

def randomly(seq):
    if seq == []:
        return []
    return random.choice(seq)

def sortmap(plist):
    if plist==[]:
        return []
    newlist = []
    newlist.append(plist[0])
    b = plist[1:4]
    b.sort()
    newlist.extend(b)
    b = plist[4:6]
    b.sort()
    newlist.extend(b)
    b = plist[6:9]
    b.sort()
    newlist.extend(b)
    b = plist[9:11]
    b.sort()
    newlist.extend(b)
    return newlist

def hashmap(thismap):
    hmap = ''
    for player in thismap:
        p = sortmap(player)
        for index,pos in enumerate(p):
            if index<9:
                s = '%d'%pos[0]+'%d'%pos[1]
                hmap = hmap + s
            else:
                s = '%d'%pos[0]+'%d'%pos[1]+'%d'%pos[2]
                hmap = hmap + s
    return hash(hmap)

"""
if __name__=='__main__':
    test=[[(1,2,0),(0,4,0),(2,1,0),(-3,-5,0),(0,0,0),(1,3,0),(0,1,0),(4,5,0),(2,2,0),(1,2,1),(1,1,0)],[]]
    hmap = hashmap(test)
    print hmap
"""
    
