#!/usr/bin/env python

import MCnode
import util
import copy

class mctree:

    def __init__(self,game,maxtry):
        self.__rootgame = game
        self.__root = MCnode.mcnode(self.__rootgame.deepCopy(),None,None)
        self.__maxtry = maxtry

    def __generateChild(self,node=None):
        if node==None:
            return
        # if the first round: put queen
        if self.__rootgame.getRound()==1:
            buffgame = node.getgame().deepCopy()
            succ = node.getgame().getSuccessor(0)
            buffgame.moveChess(0,succ[0])
            node.addChild(MCnode.mcnode(buffgame,node,[0,succ[0]]))
            print 'first round:',succ
            return
        # if not the fisrt round
        buffsucces = []
        for i in range(10):
            for s in node.getgame().getSuccessor(i):
                buffsucces.append([i,s])
        print 'succes in children generating:',buffsucces
        for succ in buffsucces:
            buffgame = node.getgame().deepCopy()
            buffgame.moveChess(succ[0],succ[1])
            node.addChild(MCnode.mcnode(buffgame,node,succ))
        if node==self.__root:
            self.__maxtry = int(self.__maxtry*len(node.getchildren()))

    def __MonteCarlo(self,currentnode):
        buffgame = currentnode.getgame().deepCopy()
        i = 0
        j = 0
        print 'MontCarlo:'
        while not buffgame.isEnd():
            succes = buffgame.getAllSuccessors()
            if succes==[]:
                buffgame.skipRound()
                j += 1
                print 'skip one step.'
                continue
            succ = util.randomly(succes)
            buffgame.moveChess(succ[0],succ[1])
            i += 1
            print 'i:',i,'j:',j
        if buffgame.isWin(self.__rootgame.getCurrentPlayer()):
            currentnode.win()
        elif buffgame.isDraw():
            currentnode.draw()
        currentnode.tryonce()

    def __traceback(self,currentnode):
        father = None
        while father != self.__root:
            father = currentnode.getfather()
            father.refreshtry_win()
            currentnode = father

    def __updateTree(self):
        currentnode = self.__root
        while (not currentnode.hasuntried()) and currentnode.haschildren():
            node = currentnode.getmaxUCT(self.__rootgame.getCurrentPlayer())
            currentnode = node
        if not currentnode.haschildren():
            self.__generateChild(currentnode)
            if not currentnode.haschildren():
                # artificial fool
                if currentnode.getgame().getCurrentPlayer()!=self.__rootgame.getCurrentPlayer():
                    currentnode.win()
                currentnode.tryonce()
		self.__traceback(currentnode)
                return
        if currentnode == self.__root and len(currentnode.getchildren())==1:
            self.__maxtry = 1
            currentnode.tryonce()
            return
	mcnode = currentnode.getuntried()
        print 'mcnode:',mcnode
        self.__MonteCarlo(mcnode)
        self.__traceback(mcnode)

    def iterating(self):
        while self.__root.gettry() < self.__maxtry:
            print 'root tried:',self.__root.gettry()
            self.__updateTree()
        print 'maxtry:',self.__maxtry
        return self.__root.choose(self.__rootgame)
