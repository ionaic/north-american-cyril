import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import * #basic Panda modules
from direct.showbase.DirectObject import DirectObject #event handling
from direct.showbase.Transitions import Transitions
from direct.actor.Actor import Actor #animated models
from direct.interval.IntervalGlobal import * #compound intervals
from direct.task import Task #update functions
import time
from MapGen import *
from Player import *
from Enemy import *

# multisampling
loadPrcFileData("", "framebuffer-multisample 1")
loadPrcFileData("", "multisamples 1")

import math, sys, random

class Play(DirectObject):
  def __init__(self, parent):
    #Turn off default mouse control
    base.disableMouse()
    base.setFrameRateMeter(True)
    #globalClock = ClockObject.getGlobalClock()
    #globalClock.setMode(ClockObject.MLimited)
    #globalClock.setFrameRate(1000)
    #Set windows properties
    self.props = WindowProperties()
    self.props.setCursorHidden(True)
    #props.setFullscreen(1)
    #props.setSize(int(base.pipe.getDisplayWidth()), int(base.pipe.getDisplayHeight()))
    self.props.setMouseMode(WindowProperties.MRelative)
    base.win.requestProperties(self.props)
    
    self.transition = Transitions(loader)
    self.transition.setFadeColor(0,0,0)
    
    self.parent = parent
    base.accept("escape", self.togglePause)
    self.setupSounds()
    self.initModels()
    self.setupCollisions()
    self.task = taskMgr.add(self.update, "updateTask")
    
    base.accept("player-into-exit", self.map.nextLevel)
  
  def fadeOut(self):
    self.transition.fadeOut(1)
    
  def fadeIn(self):
    self.transition.irisIn(1)
  
  def togglePause(self):
    if self.parent.paused:
      self.props.setCursorHidden(True)
      base.win.requestProperties(self.props)
      base.win.movePointer(0, base.win.getXSize()/2, base.win.getYSize()/2)
      taskMgr.add(self.task)
      self.parent.mainFrame.hide()
      self.parent.paused = False 
      self.playingBGM.setTime(self.bgmTime) 
      self.playingBGM.play()
    else:
      self.props.setCursorHidden(False)
      base.win.requestProperties(self.props)
      taskMgr.remove(self.task)
      self.parent.mainFrame.show()
      self.parent.paused = True
      self.bgmTime = self.playingBGM.getTime() 
      self.playingBGM.stop()
  
  def chaseBGM(self, chasing = False):
    if chasing and self.playingBGM != self.bgFast:
      self.playingBGM.stop()
      self.playingBGM = self.bgFast
      self.bgmTime = 0
      self.playingBGM.play()
    elif not chasing and self.playingBGM != self.bgSlow:
      self.playingBGM.stop()
      self.playingBGM = self.bgSlow
      self.bgmTime = 0
      self.playingBGM.play()
    
  def initModels(self):
    self.player = Player(self)
    self.map = MapGen(self.player)
    self.enemies = []
    self.level = 1
    self.startLevel(1)
  
  def transitionFunc(self, level, next = True):
    tSequence = Sequence(Func(self.fadeOut), Wait(1), Func(self.startLevel, level, next), 
                               Func(self.fadeIn))
    tSequence.start()
  
  #level number, next = true if next level (false = respawning)
  def startLevel(self, level, next = True):
    #Clear render
    self.player.clearItems()
    
    #If next level, load level map
    
      #and initialize enemies
    if next:
      enemy = Enemy( self, (0,0,0), [(0,-10,0), (0,10,0)] )
      self.enemies.append(enemy)
      self.level += 1
    
    pos = (-30,-30,6) #level.spawnPos
    walls = 3 #level.walls
    lights = 3 #level.lights
    #Spawn player using spawn (spawn pos, max walls, max lights)
    self.player.spawn(pos,walls,lights)
    if not next:
      #enemies = list of enemies in level
      for enemy in self.enemies:
        enemy.respawn()
    
    self.playingBGM = self.bgSlow
    self.playingBGM.play()
    
    
  def die(self, level, next = True):
    self.transitionFunc(level, next)
    
  def setupCollisions(self): 
    #Make a collision traverser, set it to default   
    base.cTrav = CollisionTraverser()
    base.itemTrav = CollisionTraverser()
    base.pusher = CollisionHandlerPusher()
    
    base.cHandler = CollisionHandlerEvent()
    base.queue = CollisionHandlerQueue()
    base.eQueue = CollisionHandlerQueue()
    #Set the pattern for the event sent on collision
    base.cHandler.setAgainPattern("%fn-again-%in")
    base.cHandler.setInPattern("%fn-into-%in")
    base.cHandler.setOutPattern("%fn-out-%in")
    
    self.player.initCollisions()
    for enemy in self.enemies:
      enemy.initCollisions(self.player)
    
    #base.cTrav.showCollisions(render)

  #Set up BGM
  def setupSounds(self):
    ######################slow music############################
    self.bgSlow = base.loadMusic("sounds/slow.ogg")
    self.bgSlow.setLoopCount(0)
    ######################fast music############################
    self.bgFast = base.loadMusic("sounds/fast.ogg")
    self.bgFast.setLoopCount(0)
    self.playingBGM = self.bgSlow    
    
  def update(self, task):
    dt = globalClock.getDt()
    self.player.update(globalClock.getDt())
    for enemy in self.enemies:
      enemy.update(globalClock.getDt(), self.player)
    return task.cont
