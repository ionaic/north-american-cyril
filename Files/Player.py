from pandac.PandaModules import * #basic Panda modules
from direct.showbase.DirectObject import DirectObject #event handling
import math
from Files.HUD import *

class Player(object):
  def __init__(self):
    self.speed = 70
    self.playerScale = 0.05
    self.lightDist = 1
    self.forward = Vec3(0,1,0)
    self.sprint = Vec3(0,2,0)
    self.back = Vec3(0,-1,0)
    self.left = Vec3(-1,0,0)
    self.right = Vec3(1,0,0)
    self.itemNode = NodePath('item')
    self.itemLoaded = False
    
    self.bobTimer = 0
    self.bobSpeed = 0.06
    self.bobSpeedSprint = 0.11
    self.bobAmt = 1.4
    self.bobAmtSprint = 5.2
    self.bobMid = 0
    
    self.initKeyMap()
    self.initControls()
    self.initPlayer()
    
    hud = HUD()
       
  #Initializes keyMap
  def initKeyMap(self):
    self.keyMap = {}
    self.keyMap['forward'] = 0
    self.keyMap['left'] = 0
    self.keyMap['right'] = 0
    self.keyMap['back'] = 0
    self.keyMap['sprint'] = 0
    self.abilities = {}
    self.abilities['wall'] = 0
    self.abilities['light'] = 0
    
  #Set key controls
  def initControls(self):
    #Movement
    base.accept('w', self.setKey, ['forward', 1])
    base.accept('a', self.setKey, ['left', 1])
    base.accept('d', self.setKey, ['right', 1])
    base.accept('s', self.setKey, ['back', 1])
    base.accept('w-up', self.setKey, ['forward', 0])
    base.accept('a-up', self.setKey, ['left', 0])
    base.accept('d-up', self.setKey, ['right', 0])
    base.accept('s-up', self.setKey, ['back', 0])
    #Abilities
    base.accept('shift', self.setKey, ['sprint', 1])
    base.accept('shift-up', self.setKey, ['sprint', 0])
    base.accept('1', self.toggleKey, ['wall'])
    base.accept('2', self.toggleKey, ['light'])
    base.accept('f', self.cancelKey)
    
    base.accept('mouse1', self.click)
        
  def setKey(self, key, value):
    self.keyMap[key] = value
  
  #Toggles ability
  def toggleKey(self, key):
    #Turns off other abilities if a diff ability is toggled
    for ability in self.abilities.keys():
      if ability == key:
        self.abilities[ability] += 1
      else:
        self.abilities[ability] = 0
    #Loads/removes item
    if self.abilities[key] == 1:
      self.loadItem(key)
    else:
      self.itemNode.detachNode()
      self.abilities[key] = 0
      self.itemLoaded = False
      
  #Loads passed item
  def loadItem(self, item):
    self.itemNode.detachNode()
    #Filler model
    if item == 'wall':
      self.itemNode = loader.loadModel('Models/WallTemp')
      self.itemNode.setColor(Vec4(0,1,0,1))
      self.itemNode.setScale(5)
      #Collide with env
      cNode = CollisionNode('wall')
      cSphere = CollisionSphere(0, 0, 5, 5)
      cNode.addSolid(cSphere)
      cNodePath = self.itemNode.attachNewNode(cNode)
      cNodePath.show()
      base.cTrav.addCollider(cNodePath, base.pusher)
      base.pusher.addCollider(cNodePath, self.itemNode, base.drive.node())
    else:
      self.itemNode = loader.loadModel('Models/torch')
      self.itemNode.setColor(Vec4(1,1,1,1))
      self.itemNode.setScale(2)
    #self.itemNode = loader.loadModel('Models/%s' % item)
    self.itemNode.reparentTo(self.playerNode)
    self.itemLoaded = True
    
  #Cancels ability
  def cancelKey(self):
    for ability in self.abilities.keys():
      self.abilities[ability] = 0
    self.itemLoaded = False
    self.itemNode.detachNode()
    
  #Place item when clicked, then clear loaded item
  def click(self):
    if self.itemLoaded:
      self.placeItem()
      self.cancelKey()
  def placeItem(self):
    if self.abilities['wall'] == 1:
      self.placeWall()
    elif self.abilities['light'] == 1:
      self.placeLight()
  
  #Places wall
  def placeWall(self):
    item = render.attachNewNode('item-light')
    item.setPos(self.itemNode.getPos(render))
    item.setHpr(self.itemNode.getHpr(render))
    light = loader.loadModel('Models/WallTemp')
    light.reparentTo(item)
    light.setScale(self.playerScale*5)
  
  #Places light item and creates a point light
  def placeLight(self):
    item = render.attachNewNode('item-light')
    item.setPos(self.itemNode.getPos(render))
    item.setHpr(self.itemNode.getHpr(render))
    light = loader.loadModel('Models/torch')
    light.reparentTo(item)
    light.setScale(self.playerScale*2)
    iLightNode = NodePath('ilight')
    iLightNode.reparentTo(item)
    iLight = PointLight('item-light')
    iLightNP = iLightNode.attachNewNode(iLight)
    iLightNP.node().setColor(Vec4(0.2, 0.1, 0.1, 1.0))
    iLightNP.node().setAttenuation(Vec3(0, 0.008, 0.0001))
    render.setLight(iLightNP)
      
    
  #Loads player node, camera, and light
  def initPlayer(self):
    self.playerNode = NodePath('player-node')
    #setPos depends on spawn position in level
    self.playerNode.setPos(-10,-10,3)
    self.playerNode.setScale(self.playerScale)
    self.playerNode.reparentTo(render)
    
    #Loads camera
    lens =  base.cam.node().getLens()
    lens.setFov(75)
    base.cam.node().setLens(lens)
    base.camera.reparentTo(self.playerNode)
    #Loads artifact point light
    self.pLightNode = NodePath('light-node')
    self.pLightNode.reparentTo(self.playerNode)
    self.pLightNode.setPos(Vec3(0,self.lightDist,0))
    pLight = PointLight('player-light')
    pLightNP = self.pLightNode.attachNewNode(pLight)
    pLightNP.node().setColor(Vec4(0.1, 0.1, 0.1, 1.0))
    pLightNP.node().setAttenuation(Vec3(0, 0.01, 0.0001))
    
    render.setLight(pLightNP)
    
  def initCollisions(self, cHandler):
    #Collide with env
    cNode = CollisionNode('player')
    cSphere = CollisionSphere(0, 0, -1/self.playerScale, 5)
    cNode.addSolid(cSphere)
    cNodePath = self.playerNode.attachNewNode(cNode)
    cNodePath.show()
    base.cTrav.addCollider(cNodePath, base.pusher)
    base.pusher.addCollider(cNodePath, self.playerNode, base.drive.node())
  
  #Updates player
  def update(self, dt):
    self.moveCam()
    self.movePlayer(dt)
  
  #Moves camera
  def moveCam(self):
    mouse = base.win.getPointer(0) 
    x = mouse.getX() 
    y = mouse.getY() 
    if base.win.movePointer(0, base.win.getXSize()/2, base.win.getYSize()/2): 
      self.playerNode.setH(self.playerNode.getH() - (x - base.win.getXSize()/2)*.1)
      #Move camera based on if ability is toggled
      if self.itemLoaded:
        self.moveItem(y)
      else:
        cam_p = base.camera.getP() - (y - base.win.getYSize()/2)*.1
        if cam_p >= -90 and cam_p <= 90:
          base.camera.setP(cam_p)
    #Moves pitch of player light based on camera pitch
    rad = deg2Rad(base.camera.getP())
    self.pLightNode.setPos(0,self.lightDist*math.cos(rad)/self.playerScale,
                           self.lightDist*math.sin(rad)/self.playerScale)
  
  #Moves item and camera if ability is toggled
  def moveItem(self, y):
    cam_p = base.camera.getP() - (y - base.win.getYSize()/2)*.1
    if cam_p >= -90 and cam_p <= -20:
      base.camera.setP(cam_p)
    elif cam_p > -20:
      base.camera.setP(-20)
    
    rad = deg2Rad(base.camera.getP())
    itemDist = self.playerNode.getZ()/-math.tan(rad)
    self.itemNode.setFluidPos(Vec3(0,itemDist/self.playerScale,
                         -1*self.playerNode.getZ()/self.playerScale))
    heading = self.playerNode.getH()
    heading = (int(heading) % 180)
    if (heading >= 60 and heading < 120):
      self.itemNode.setH(render, 90)
    elif (heading >= 30 and heading < 60):
      self.itemNode.setH(render, 45)
    elif (heading >= 120 and heading < 150):
      self.itemNode.setH(render, 135)
    else:
      self.itemNode.setH(render, 0)
    
  #Move player based on key movements
  def movePlayer(self, dt):
    bobAmt = self.bobAmt
    bobSpeed = self.bobSpeed
    if self.keyMap['forward'] == 1:
      if self.keyMap['sprint'] == 1:
        forward = self.sprint
        bobAmt = self.bobAmtSprint
        bobSpeed = self.bobSpeedSprint
      else:
        forward = self.forward
      self.playerNode.setPos(self.playerNode, forward * dt * self.speed)
    elif self.keyMap['back'] == 1:
      self.playerNode.setPos(self.playerNode, self.back * dt * self.speed)
    
    if self.keyMap['left'] == 1:
      self.playerNode.setPos(self.playerNode, self.left * dt * self.speed)
    elif self.keyMap['right'] == 1:
      self.playerNode.setPos(self.playerNode, self.right * dt * self.speed)
      
    #Head bobbing
    if (self.keyMap['forward'] + self.keyMap['back'] +
        self.keyMap['left'] + self.keyMap['right']) >= 1:
      self.bobTimer = (self.bobTimer + bobSpeed) % (math.pi * 2)
      self.headBob(bobAmt)
  
  def headBob(self, bobAmt):
    waveslice = math.sin(self.bobTimer)
    if waveslice != 0:
      change = waveslice * self.bobAmt
      base.camera.setZ(self.bobMid + change)
    else:
      base.camera.setZ(self.bobMid)
    
  
    
