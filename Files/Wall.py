from pandac.PandaModules import * #basic Panda modules
from direct.showbase.DirectObject import DirectObject #event handling

class Wall:
    def __init__(self, modelPath = ""):
        self.model = None # wall model nodepath
        
