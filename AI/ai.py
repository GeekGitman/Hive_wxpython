#!/usr/bin/env python

import MCtree as mc

class ai:

    def __init__(self,game):
        self.__maxtry = 50
        self.__game = game

    def play(self):
        mct = mc.mctree(self.__game,self.__maxtry)
        print "AI playing..."
        currentmap = mct.iterating()
        return currentmap
