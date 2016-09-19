
import wx

class chesspanel(wx.Panel):

    def __init__(self,parent,ID,game=None):
        wx.Panel.__init__(self,parent,ID,style=wx.SUNKEN_BORDER)
        self.SetSize((250,900))
        self.SetPosition(wx.Point(1600,50))
        self.parent = parent
        self.SetBackgroundColour("WHITE")
        self.loadbitmap()
        self.createButton()
        self.Game = game
        self.b = {'b_queen':[0,0],'w_queen':[1,0],'b_ant':[0,3],'w_ant':[1,3],'b_spider':[0,5],'w_spider':[1,5],'b_cricket':[0,8],'w_cricket':[1,8],'b_beetle':[0,10],'w_beetle':[1,10]}

    def loadbitmap(self):
        self.bitmaps = {}
        name = ['b_queen','b_ant','b_spider','b_cricket','b_beetle','w_queen','w_ant','w_spider','w_cricket','w_beetle','green','red']
        for i in range(12):
            self.bitmaps[name[i]]=wx.Bitmap('./layout/bitmaps/'+'%d'%i+'.png',wx.BITMAP_TYPE_PNG)

    def createButton(self):   
        self.queen = wx.BitmapButton(self,-1,self.bitmaps['b_queen'],pos=(50,25),size=(150,150),name='b_queen')
        self.queentext = wx.StaticText(self,-1,'1',pos=(125,175),size=(150,20),style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.ant = wx.BitmapButton(self,-1,self.bitmaps['b_ant'],pos=(50,195),size=(150,150),name='b_ant')
        self.anttext = wx.StaticText(self,-1,'3',pos=(125,345),size=(150,20),style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.spider = wx.BitmapButton(self,-1,self.bitmaps['b_spider'],pos=(50,365),size=(150,150),name='b_spider')
        self.spidertext = wx.StaticText(self,-1,'2',pos=(125,515),size=(150,20),style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.cricket = wx.BitmapButton(self,-1,self.bitmaps['b_cricket'],pos=(50,535),size=(150,150),name='b_cricket')
        self.crickettext = wx.StaticText(self,-1,'3',pos=(125,685),size=(150,20),style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.beetle = wx.BitmapButton(self,-1,self.bitmaps['b_beetle'],pos=(50,705),size=(150,150),name='b_beetle')
        self.beetletext = wx.StaticText(self,-1,'2',pos=(125,855),size=(150,20),style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.Bind(wx.EVT_BUTTON,self.OnClick,self.queen)
        self.Bind(wx.EVT_BUTTON,self.OnClick,self.ant)
        self.Bind(wx.EVT_BUTTON,self.OnClick,self.spider)
        self.Bind(wx.EVT_BUTTON,self.OnClick,self.cricket)
        self.Bind(wx.EVT_BUTTON,self.OnClick,self.beetle)
        self.Bind(wx.EVT_RIGHT_UP,self.OnRightClick)
    
    def OnRightClick(self,evt):
        self.parent.panel_map.unsetFocus()

    def OnClick(self,evt):
        button = evt.GetEventObject()
        name = button.GetName()
        # ask for legal state
        chessid = self.b[name]
        if (not self.parent.panel_map.mapcopy==[]) and button.GetParent()==self:
            inmap = self.parent.panel_map.mapcopy[0][self.Game.getCurrentPlayer()]
            while inmap[chessid[1]]!=[0,0,-1]:
                chessid[1] = chessid[1]-1
        legal = self.Game.getSuccessor(chessid[1])
        self.parent.panel_map.setFocus(chessid[1],legal)

    def switchPlayer(self,nowplayer):
        a = {'b_queen':'w_queen','w_queen':'b_queen','b_ant':'w_ant','w_ant':'b_ant','b_spider':'w_spider','w_spider':'b_spider','b_cricket':'w_cricket','w_cricket':'b_cricket','b_beetle':'w_beetle','w_beetle':'b_beetle'}
        b = {'b_queen':[0,0],'w_queen':[1,0],'b_ant':[0,3],'w_ant':[1,3],'b_spider':[0,5],'w_spider':[1,5],'b_cricket':[0,8],'w_cricket':[1,8],'b_beetle':[0,10],'w_beetle':[1,10]}
        newname = [a[self.queen.GetName()],a[self.ant.GetName()],a[self.spider.GetName()],a[self.cricket.GetName()],a[self.beetle.GetName()]]
        if 1==1:
            self.queen.SetBitmapLabel(self.bitmaps[newname[0]])
            self.queen.SetName(newname[0])
            buff = self.Game.getChessNum(b[self.queen.GetName()])
            self.queentext.SetLabel('%d'%buff)
            if buff==0:
                self.queen.Disable()
            else:
                self.queen.Enable()
            #######
            self.ant.SetBitmapLabel(self.bitmaps[newname[1]])
            self.ant.SetName(newname[1])
            buff = self.Game.getChessNum(b[self.ant.GetName()])
            self.anttext.SetLabel('%d'%buff)
            if buff==0:
                self.ant.Disable()
            else:
                self.ant.Enable()
            #######
            self.spider.SetBitmapLabel(self.bitmaps[newname[2]])
            self.spider.SetName(newname[2])
            buff = self.Game.getChessNum(b[self.spider.GetName()])
            self.spidertext.SetLabel('%d'%buff)
            if buff==0:
                self.spider.Disable()
            else:
                self.spider.Enable()
            #######
            self.cricket.SetBitmapLabel(self.bitmaps[newname[3]])
            self.cricket.SetName(newname[3])
            buff = self.Game.getChessNum(b[self.cricket.GetName()])
            self.crickettext.SetLabel('%d'%buff)
            if buff==0:
                self.cricket.Disable()
            else:
                self.cricket.Enable()
            #######
            self.beetle.SetBitmapLabel(self.bitmaps[newname[4]])
            self.beetle.SetName(newname[4])
            buff = self.Game.getChessNum(b[self.beetle.GetName()])
            self.beetletext.SetLabel('%d'%buff)
            if buff==0:
                self.beetle.Disable()
            else:
                self.beetle.Enable()
        if nowplayer=='AI':
            self.queen.Disable()
            self.ant.Disable()
            self.spider.Disable()
            self.cricket.Disable()
            self.beetle.Disable()
        self.Update()            
