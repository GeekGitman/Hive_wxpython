
import wx
from panel1 import chesspanel
from panel2 import mappanel
import gc

class topframe(wx.Frame):

    def __init__(self,parent,name,game,ai):
        wx.Frame.__init__(self,parent,-1,name,style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER & wx.MAXIMIZE_BOX))
        self.SetSize((1920,1080))
        self.setMenu()
        self.setStatusBar()
        self.Centre()
        self.Game = game
        self.AI = ai
        self.Players = None
        self.nowPlayer = None
        self.panel_chess = chesspanel(self,-1,self.Game)
        self.panel_chess.Show(False)
        self.panel_map = mappanel(self,-1,game=self.Game)
        self.panel_map.Show(False)

    def setMenu(self):
        menuBar = wx.MenuBar()
        startmenu = wx.Menu()
        single = startmenu.Append(wx.ID_ANY,'G&ame with AI')
        double = startmenu.Append(wx.ID_ANY,'D&ouble Players')
        startmenu.AppendSeparator()
        restart = startmenu.Append(wx.ID_ANY,'R&estart')
        quit = startmenu.Append(wx.ID_EXIT,'&Quit')
        menuBar.Append(startmenu,'&Start')
        self.Bind(wx.EVT_MENU,self.OnSingle,single)
        self.Bind(wx.EVT_MENU,self.OnDouble,double)
        self.Bind(wx.EVT_MENU,self.OnExit,quit)
        self.Bind(wx.EVT_RIGHT_UP,self.OnRightClick)
        self.Bind(wx.EVT_MENU,self.OnRestart,restart)
        self.SetMenuBar(menuBar)

    def setStatusBar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText('Ready.No Players.')
    
    def OnRestart(self,evt):
        self.statusbar.SetStatusText('Ready.No Players.')
        self.Players = None
        self.nowPlayer = None
        self.panel_chess.Destroy()
        self.panel_map.Destroy()
        self.panel_chess = chesspanel(self,-1,self.Game)
        self.panel_chess.Show(False)
        self.panel_map = mappanel(self,-1,game=self.Game)
        self.panel_map.Show(False)
        self.Game.restart()

    def OnRightClick(self,evt):
        self.panel_map.unsetFocus()

    def OnSingle(self,evt):
        result = None
        if self.nowPlayer==None:
            Priori = wx.MessageDialog(None,"Do you want to play first?",'Choose priori',wx.YES_NO|wx.CANCEL)
            result = Priori.ShowModal()
        if result==wx.ID_CANCEL:
                return
        elif result==wx.ID_NO:
            self.Players = {'Black':'AI','White':'Human'}
            self.nowPlayer = 'Black'
            self.Game.setNumOfPlayers(1)
            self.panel_map.Show(True)
            self.panel_chess.Show(True)
            self.panel_map.Disable()
            self.statusbar.SetStatusText('Single player.'+self.Players[self.nowPlayer])
            self.panel_map.NextforAI(self.AI.play())
            self.panel_map.Enable()
        elif result==wx.ID_YES:
            self.Players = {'Black':'Human','White':'AI'}
            self.nowPlayer = 'Black'
            self.Game.setNumOfPlayers(1)
            self.panel_map.Show(True)
            self.panel_chess.Show(True)
            self.statusbar.SetStatusText('In turns now: '+self.Players[self.nowPlayer])
        else:
            ex = {'Black':'White','White':'Black'}
            self.Players = {self.nowPlayer:'AI',ex[self.nowPlayer]:'Human'}
            self.Game.setNumOfPlayers(1)
            self.panel_map.Disable()
            self.statusbar.SetStatusText('Single player.'+self.Players[self.nowPlayer])
            self.panel_map.NextforAI(self.AI.play())
            self.panel_map.Enable()

    def OnDouble(self,evt):
        self.Game.setNumOfPlayers(2)
        self.panel_map.Show(True)
        self.panel_chess.Show(True)
        self.Players = {'Black':'Human_1','White':'Human_2'}
        if self.nowPlayer==None:
            self.nowPlayer = 'Black'
        self.statusbar.SetStatusText('In turns now: '+self.Players[self.nowPlayer])

    def OnExit(self,evt):
        self.Close()
   
    """
    def switchPlayer(self):
        a = {'Black':'White','White':'Black'}
        self.nowPlayer = a[self.nowPlayer]
        self.panel_chess.switchPlayer(self.Players[self.nowPlayer])
        self.statusbar.SetStatusText('In turns now: '+self.Players[self.nowPlayer])
        if self.Players[self.nowPlayer]=='AI':
            self.panel_map.Disable()
            self.panel_map.NextforAI(self.AI.play())
            self.panel_map.Enable()
    """

    def win(self,player):
        sh = wx.MessageDialog(None,player+" player win!",'Game Over',wx.OK)
        sh.ShowModal()
        self.OnRestart(None)

    def draw(self):
        sh = wx.MessageDialog(None,"Game ends in a draw!",'Game Over',wx.OK)
        sh.ShowModal()
        self.OnRestart(None)

    def skiponce(self,player):
        sh = wx.MessageDialog(None,player+" have no legal action for the next step! Press OK to continue...",'Message',wx.OK)
        sh.ShowModal()
