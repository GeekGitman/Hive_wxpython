
import wx

class mappanel(wx.Panel):
    
    def __init__(self,parent,ID,game=None):
        wx.Panel.__init__(self,parent,ID,style=wx.SUNKEN_BORDER)
        self.SetSize((1500,900))
        self.SetPosition(wx.Point(50,50))
        self.parent = parent
        self.Game = game
        self.shift = (0,0)
        self.SetBackgroundColour("LIGHT GREY")
        #self.mapcopy = [[[[0, 0, 1], [1, 0, 1], [-1, 0, 1], [1, -1, 1], [0, -1, 1], [0, 0, -1], [1, 1, 1], [0, 0, -1], [0, 0, -1], [0, 0, -1], [0, 0, -1]], [[0, 1, 1], [2, 3, 1], [2, 1, 1], [0, 0, -1], [0, 0, -1], [0, 0, -1], [1, 3, 1], [0, 0, -1], [0, 0, -1], [1, 2, 1], [0, 0, -1]]], [1, -1, 1]]
        self.mapcopy = []
        self.focus = None       # [id of chess that cause focus]
        self.focuspoint = []    # [[logical],[physics]]
        self.images = []
        self.bx = [['b_queen','b_ant','b_ant','b_ant','b_spider','b_spider','b_cricket','b_cricket','b_cricket','b_beetle','b_beetle'],['w_queen','w_ant','w_ant','w_ant','w_spider','w_spider','w_cricket','w_cricket','w_cricket','w_beetle','w_beetle']]
        # bind triggers
        self.Bind(wx.EVT_RIGHT_UP,self.OnRightClick)
        self.Bind(wx.EVT_MOTION,self.drag)
        self.Bind(wx.EVT_LEFT_DOWN,self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP,self.OnLeftUp)
        #self.flushmap()

    def OnLeftDown(self,evt):
        self.__motion = evt.GetPosition()
        self.__cpos = []
        self.__gpos = []
        if self.images != []:
            for chess in self.images:
                self.__cpos.append(chess.GetPosition())
        if self.focuspoint != []:
            for greens in self.focuspoint[1]:
                self.__gpos.append(greens)

    def OnLeftUp(self,evt):
        pos = evt.GetPosition()
        self.shift = [pos[0]-self.__motion[0],pos[1]-self.__motion[1]]
        self.__motion = None
        self.__cpos = None
        self.__gpos = None
        print self.shift

    def drag(self,evt):
        try:
            self.images[0]
            if self.__motion == None:
                return
        except:
            return
        pos = evt.GetPosition()
        relative = (pos[0]-self.__motion[0],pos[1]-self.__motion[1])
        if self.images != []:
            for index,chess in enumerate(self.images):
                buff = self.__cpos[index]
                chess.SetPosition((buff[0]+relative[0],buff[1]+relative[1]))
        if self.focuspoint != []:
            for index,greens in enumerate(self.focuspoint[1]):
                self.focuspoint[1][index] = [self.__gpos[index][0]+relative[0],self.__gpos[index][1]+relative[1]]
        self.shift = relative
        self.Update()
    
    def OnRightClick(self,evt):
        self.unsetFocus()

    def OnNext(self,evt):
        selected = evt.GetEventObject()
        position = selected.GetPosition()
        position = [position[0]+70,position[1]+61]
        logical = self.focuspoint[0][self.focuspoint[1].index(position)]
        print 'beforeMove:',self.focus,logical
        self.Game.moveChess(self.focus%20,logical)
        print 'Movechess=>',self.focus,'to',logical
        nowplayers=['Black','White']
        # flush map
        self.mapcopy = self.Game.getCurrentState()
        self.unsetFocus()
        # whether it is a draw
        if self.Game.isDraw():
            self.parent.draw()
            return
        # iswin or lose?
        if self.Game.isWin(self.Game.getCurrentPlayer()):
            self.parent.win(nowplayers[self.Game.getCurrentPlayer()])
            return
        if self.Game.isLose(self.Game.getCurrentPlayer()):
            self.parent.win(nowplayers[abs(self.Game.getCurrentPlayer()-1)])
            return
        # whether nextone has legal action:
        if self.Game.hasNext():
            self.parent.skiponce(nowplayers[self.Game.getCurrentPlayer()])
            self.Game.skipRound()
            return
        # if nextone is AI :
        if self.parent.Players[nowplayers[self.Game.getCurrentPlayer()]]=='AI':
            self.parent.panel_chess.switchPlayer(self.parent.Players[nowplayers[self.Game.getCurrentPlayer()]])
            self.Disable()
            self.NextforAI(self.parent.AI.play())
            self.Enable()
            return
        # nextone is human:
        self.parent.panel_chess.switchPlayer(self.parent.Players[nowplayers[self.Game.getCurrentPlayer()]])
            
    def NextforAI(self,nextstate):
        self.mapcopy = nextstate
        self.flushmap()
        # whether it is a draw
        if self.Game.isDraw():
            self.parent.draw()
            return
        # iswin or lose?
        nowplayers=['Black','White']
        if self.Game.isWin(self.Game.getCurrentPlayer()):
            self.parent.win(nowplayers[self.Game.getCurrentPlayer()])
            return
        if self.Game.isLose(self.Game.getCurrentPlayer()):
            self.parent.win(nowplayers[abs(self.Game.getCurrentPlayer()-1)])
            return
        # whether nextone has legal action:
        if self.Game.hasNext():
            self.parent.skiponce(nowplayers[self.Game.getCurrentPlayer()])
            self.Game.skipRound()
            return
        self.parent.panel_chess.switchPlayer(self.parent.Players[nowplayers[self.Game.getCurrentPlayer()]])


    def OnClickImage(self,evt):
        image = evt.GetEventObject()
        chessid = int(image.GetName())
        print 'Try image:',chessid,self.Game.getCurrentPlayer()
        if (self.Game.getCurrentPlayer()*20+1-20)*(chessid+1-20)<0:
            return
        print 'Click image:',chessid,self.Game.getCurrentPlayer()
        legal = self.Game.getSuccessor(chessid%20)
        self.setFocus(chessid,legal)

    def cortrans(self,logical):
        physics = []
        for cor in logical:
            if cor==[0,0,-1]:
                physics.append(None)
            else:
                physics.append([750+105*cor[0]+self.shift[0],450-122*cor[1]+61*cor[0]+self.shift[1]])
        return physics

    def setFocus(self,chessid,legalposition):
        physics = self.cortrans(legalposition)
        self.focus = chessid
        self.focuspoint = [legalposition,physics]
        print 'setfocus=>',self.focus,':',self.focuspoint
        self.flushmap()

    def unsetFocus(self):
        if self.focus==None:
            return
        self.focus = None
        self.focuspoint = []
        print 'unsetfocus;'
        self.flushmap()
 
    def flushmap(self):
        # paint self.mapcopy[] first
        # paint focus point then
        for m in self.images:
            m.Destroy()
            self.Update()
        self.images = []
        # paint focus point at the bottom if this is beetle
        if self.focuspoint==[]:
            self.Refresh()
        else:
            for bmp in self.focuspoint[1]:
                pos = (bmp[0]-70,bmp[1]-61)
                buff = wx.StaticBitmap(self,-1,self.parent.panel_chess.bitmaps['green'],pos,name='green')
                self.images.append(buff)
                self.images[-1].Bind(wx.EVT_LEFT_UP,self.OnNext)
        # paint chess
        if self.mapcopy==[]:
            self.Refresh()
        else:
            beetledis = [None,-1,'']
            for cplayer in [0,1]:
                for ind,chess in enumerate(self.mapcopy[0][cplayer]):
                    if chess==[0,0,-1]:
                        continue
                    bmp = self.cortrans([chess])
                    pos = (bmp[0][0]-70,bmp[0][1]-61)
                    buff = wx.StaticBitmap(self,-1,self.parent.panel_chess.bitmaps[self.bx[cplayer][ind]],pos,name='%d'%(cplayer*20+ind))
                    buff.Bind(wx.EVT_LEFT_UP,self.OnClickImage)
                    self.images.append(buff)
                    if (ind==9 or ind==10) and beetledis[1]<chess[2]:
                        beetledis = [pos,chess[2],buff.GetName()]
            # handel beetles
            for chess in self.images:
                if chess.GetPosition()==beetledis[0] and chess.GetName()!=beetledis[2] and chess.GetName()!='green':
                    chess.Show(False)
            # paint last step
            pos = self.cortrans([self.mapcopy[1]])
            if pos[0]!=None:
                pos = (pos[0][0]-70,pos[0][1]-61)
                buff = wx.StaticBitmap(self,-1,self.parent.panel_chess.bitmaps['red'],pos)
                self.images.append(buff)
        # paint focus point
        if self.focuspoint==[]:
            self.Refresh()
        else:
            for bmp in self.focuspoint[1]:
                pos = (bmp[0]-70,bmp[1]-61)
                buff = wx.StaticBitmap(self,-1,self.parent.panel_chess.bitmaps['green'],pos)
                self.images.append(buff)
                self.images[-1].Bind(wx.EVT_LEFT_UP,self.OnNext)
        #
        self.Refresh()
        print 'flushmap:end'
