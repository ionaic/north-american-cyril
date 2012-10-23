# io.py
# panda imports
from pandac.PandaModules import * #basic Panda modules
from direct.showbase.DirectObject import DirectObject #for event handling

# system imports


# local imports

class IOHandler:
    # basic keys to accept
    defaultKeys = ("arrow_up" \
        , "arrow_left" \
        , "arrow_right" \
        , "arrow_down" \
        , "arrow_up-up" \
        , "arrow_left-up" \
        , "arrow_right-up" \
        , "arrow_down-up")
    # secondary keys to accept
    defaultKeys2 = ("w" \
        , "a" \
        , "d" \
        , "s" \
        , "w-up" \
        , "a-up" \
        , "d-up" \
        , "s-up")
    # default arguments to pass to the key events
    defaultArgs = (["forward", 1] \
        , ["left", 1] \
        , ["right", 1] \
        , ["back", 1] \
        , ["forward", 0] \
        , ["left", 0] \
        , ["right", 0] \
        , ["back", 0])
        
    def __init__(self, charToControl):
        