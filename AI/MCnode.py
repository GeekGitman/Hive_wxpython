#!/usr/bin/env python

import util
import math

class mcnode:

    def __init__(self,game,father,lastmove):
        self.__game = game
        self.__maphash = util.hashmap(game.normalize()[0])
        self.__trytime = 0
        self.__wintime = 0
        self.__uct = 0
        self.__father = father
        self.__children = []
        self.__untriedchildren = []
        self.__last = lastmove

    def getLast(self):
        return self.__last

    def getgame(self):
        return self.__game

    def haschildren(self):
        if self.__children == []:
            return False
        return True

    def hasuntried(self):
        if self.__untriedchildren!=[]:
            return True
        return False

    def getuntried(self):
        if not self.hasuntried():
            return None
        t = util.randomly(self.__untriedchildren)
        self.__untriedchildren.remove(t)
        return t

    def getchildren(self):
        return self.__children

    def getmaxUCT(self,player):
        if self.__children == []:
            return None
        uct = []
        if self.__game.getCurrentPlayer()==player:
            for child in self.__children:
                uct.append(child.getwin()/float(child.gettry())+math.sqrt(2*math.log(self.gettry(),math.e)/float(child.gettry())))
        else:
            for child in self.__children:
                uct.append(1-child.getwin()/float(child.gettry())+math.sqrt(2*math.log(self.gettry(),math.e)/float(child.gettry())))
        if max(uct) == 0:
            return self.getchild()
        else:
            return self.__children[uct.index(max(uct))]

    def getchild(self):
        if self.__children == []:
            return None
        return util.randomly(self.__children)

    def choose(self,rootgame):
        #trytimes = [child.gettry() for child in self.__children]
        if len(self.__children)==1:
            nextnode = self.__children[0]
            rootgame.moveChess(nextnode.getLast()[0],nextnode.getLast()[1])
            return nextnode.getgame().getCurrentState()
        func = [float(child.getwin())/child.gettry() for child in self.__children]
        maxfun = max(func)
        index = []
        for i,rate in enumerate(func):
            if rate == maxfun:
                index.append(i)
        ind = util.randomly(index)
        nextnode = self.__children[ind]
        rootgame.moveChess(nextnode.getLast()[0],nextnode.getLast()[1])
        if nextnode.gettry()!=0:
            print 'amount of children:',len(self.__children)
            print 'win time of selected action:',nextnode.getwin()
            print 'try time of selected action:',nextnode.gettry()
            print 'win rate:',float(nextnode.getwin())/nextnode.gettry()
            print 'win rate list:',func
        return nextnode.getgame().getCurrentState()

    def gettry(self):
        return self.__trytime

    def getwin(self):
        return self.__wintime

    def getfather(self):
        return self.__father

    def getmap(self):
        return self.__maphash

    def tryonce(self):
        self.__trytime += 1
  
    def win(self):
        self.__wintime += 1

    def draw(self):
        self.__wintime += 0.5

    def refreshtry_win(self): 
        self.__trytime = 0
        self.__wintime = 0
        for child in self.__children:
            self.__trytime += child.gettry()
            self.__wintime += child.getwin()

    def addChild(self,child):
        ch_now = [i.getmap() for i in self.__children]
        if ch_now.count(child.getmap())>0:
            return
        self.__children.append(child)
        self.__untriedchildren.append(child)
