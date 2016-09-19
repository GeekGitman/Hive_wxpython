import wx
from mainFrame import topframe

class ChessApp(wx.App):

    def __init__(self,redirect=False,game=None,ai=None):
        self.redirectFile = '/mnt/share/chess/test.txt'
        self.Game = game
        self.AI = ai
        wx.App.__init__(self,redirect,self.redirectFile)

    def OnInit(self):
        TopFrame = topframe(parent=None,name='chessgame',game=self.Game,ai=self.AI)
        TopFrame.Show(True)
        self.SetTopWindow(TopFrame)
        return True
