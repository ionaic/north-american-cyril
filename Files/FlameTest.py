from pandac.PandaModules import loadPrcFileData # loading prc files
loadPrcFileData("", "framebuffer-multisample 1")
loadPrcFileData("", "multisamples 1")
#loadPrcFileData("", "fullscreen #t")
#loadPrcFileData("", "window-resolution x y")
# global python imports
import math, sys, random
#-----------------------------------------------------------------------------
# Panda imports
import direct.directbase.DirectStart #starts panda
from pandac.PandaModules import * #basic Panda modules
from direct.showbase.DirectObject import DirectObject #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import * #for compound intervals
from direct.task import Task #for update functions

from panda3d.core import Shader #attempted to get shaders working
from direct.particles.ParticleEffect import ParticleEffect #attempted to get particle effects working


class FlameTest:
    def __init__(self):
        self.setupLights()
        self.loadItem()
        self.loadParticles()
    
    
    def loadItem(self):
        self.itemNode = loader.loadModel('../Models/torch')
        self.itemNode.setColor(Vec4(1,1,1,1))
        self.itemNode.setScale(2)
        self.itemNode.reparentTo(render)
        self.itemNode.setPos(0,0,0)

    def loadParticles(self):
        base.enableParticles()
        self.rFlame = ParticleEffect()
        self.rFlame.loadConfig("../Models/fire.ptf")
        self.rFlame.start(self.itemNode)
        pos = self.itemNode.getPos()
        self.rFlame.setPos(pos[0], pos[1], pos[2] + 4)
        
    
    def setupLights(self):
        # set up an ambient light
        self.ambientLight = AmbientLight("ambientLight")
        
        #for setting colors, alpha is largely irrelevant
        # slightly blue to try and produce a wintry, snowy look
        self.ambientLight.setColor((1, 1, 1, 1.0))
        
        #create a NodePath, and attach it directly into the scene
        self.ambientLightNP = render.attachNewNode(self.ambientLight)
        
        #the node that calls setLight is what's illuminated by the given light
        #you can use clearLight() to turn it off
        render.setLight(self.ambientLightNP)

test = FlameTest()
run()
