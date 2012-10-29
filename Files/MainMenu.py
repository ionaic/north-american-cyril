from direct.gui.DirectGui import *

class MainMenu:
    def __init__(self, parent):
        
        self.mainFrame = DirectFrame(
                                     frameColor=(0,0,0,1),
                                     #(left, right, bottom, top)
                                     frameSize=(-1.2,-0.6,0.9,-0.2 )
                                     )
        
        self.start = DirectButton(
                                  parent = self.mainFrame, 
                                  text = ("Start"), 
                                  pos = (-1,0,0.6),
                                  scale=.1,
                                  command = parent.startGame
                                  )    
        
        self.exit = DirectButton(
                                 parent = self.mainFrame, 
                                 text = ("Exit"), 
                                 pos = (-1.065,0,0.2),
                                 scale=.1,
                                 command = parent.exit)
        
    def hide(self):
        self.mainFrame.hide()
        
    def show(self):
        self.mainFrame.show()

    
    #TODO: check this
    def __del__(self):
        self.start.destroy()
        self.exit.destroy()
        self.mainFrame.destroy()
