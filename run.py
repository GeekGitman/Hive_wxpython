#!usr/bin/env python

import sys
sys.path.append('layout')
sys.path.append('game')
sys.path.append('AI')
import wx
import app
import Game
import ai

if __name__=='__main__':
    thisGame = Game.Game()
    thisAI = ai.ai(thisGame)
    thisapp = app.ChessApp(game=thisGame,ai=thisAI)
    thisapp.MainLoop()

