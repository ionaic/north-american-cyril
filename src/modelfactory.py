from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import * #for compound intervals
from direct.task import Task #for update functions

# CLASS: ModelFactory
# INTENT: Factory object to create actors
class ModelFactory:
    # ------ARGUMENTS------
    # eggPath (string): path to the egg file (string)
    # position (tuple(3) or list(3)): optional argument to set the 
    #   position; should be a 3 element list or tuple
    # scale (double): optional argument to set the scale of the model
    # desiredParent (NodePath): optional argument to choose a parent other than 
    #   render
    # collisions (list): list of collision objects to load onto the model from
    #   the same file
    # lights (list(list(3)): optional argument, list of 3 element lists/tuples 
    #   indicating lights. the lists/tuples are structured as ("**/name", #   color)
    def loadModel(eggPath, position = [0,0,0],\
        scale = 1, desiredParent = render, collisions = [], lights = []):
        try:
            mod = loader.loadModel(eggPath)
            mod.reparentTo(desiredParent)
            mod.setPos(position[0], position[1], position[2])
            mod.setScale(scale)
            for cObj in collisions:
                ModelFactory.loadCollisionObj(cObj, mod)
            for lObj in lights:
                ModelFactory.loadLightFromEgg(mod, lObj[0], lObj[1])
            return mod
        except ValueError:
            print("Model at " + str(eggPath) + " not found.")
            
    def loadLightFromEgg(parent, name, color):
        light_orig = parent.find(name)
        light = PointLight(name)
        light.setColor(color)
        lightNP = parent.attachNewNode(
        
    
    def loadCollisionObj(colObj, parent):
        