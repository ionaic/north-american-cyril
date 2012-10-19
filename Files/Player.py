from pandac.PandaModules import * #basic Panda modules
from direct.showbase.DirectObject import DirectObject #event handling
import math

class Player(object):
  def __init__(self):
    self.speed = 100
    self.lightDist = 15
    self.forward = Vec3(0,1,0)
    self.back = Vec3(0,-1,0)
    self.left = Vec3(-1,0,0)
    self.right = Vec3(1,0,0)
    
    self.initKeyMap()
    self.initControls()
    self.initPlayer()
       
  #Initializes keyMap
  def initKeyMap(self):
    self.keyMap = {}
    self.keyMap['forward'] = 0
    self.keyMap['left'] = 0
    self.keyMap['right'] = 0
    self.keyMap['back'] = 0
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
    base.accept('1', self.toggleKey, ['wall'])
    base.accept('2', self.toggleKey, ['light'])
    base.accept('f', self.cancelKey)
        
  def setKey(self, key, value):
    self.keyMap[key] = value
  
  #Toggles ability
  def toggleKey(self, key):
    for ability in self.abilities.keys():
      if ability != key:
        self.abilities[ability] = 0
    self.abilities[key] = (self.abilities[key] + 1) % 3
    
  #Cancels ability
  def cancelKey(self):
    for ability in self.abilities.keys():
      self.abilities[ability] = 0
    
  #Loads player node, camera, and light
  def initPlayer(self):
    self.playerNode = NodePath('player-node')
    self.playerNode.setPos(-10,-10,3)
    self.playerNode.setScale(0.05)
    self.playerNode.reparentTo(render)
    
    #Loads camera
    lens =  base.cam.node().getLens()
    lens.setFov(75)
    base.cam.node().setLens(lens)
    base.camera.reparentTo(self.playerNode)
    
    #Testing light location
    self.test = loader.loadModel('Models/sphere')
    self.test.reparentTo(self.playerNode)
    self.test.setTwoSided(True)
    self.test.setPos(Vec3(0,self.lightDist,0))
    
    #Loads artifact point light
    self.pLightNode = NodePath('light-node')
    self.pLightNode.reparentTo(self.playerNode)
    self.pLightNode.setPos(Vec3(0,self.lightDist,0))
    pLight = PointLight('player-light')
    pLightNP = self.pLightNode.attachNewNode(pLight)
    pLightNP.node().setColor(Vec4(0.1, 0.2, 0.2, 1.0))
    pLightNP.node().setAttenuation(Vec3(0, 0.001, 0.0001))
    
    render.setLight(pLightNP)
    
  def initCollisions(self, pusher, cHandler):
    #Collide with env
    cNode = CollisionNode('player')
    cSphere = CollisionSphere(0, 0, 4, 10)
    cNode.addSolid(cSphere)
    cNodePath = self.playerNode.attachNewNode(cNode)
    cNodePath.show()
    base.cTrav.addCollider(cNodePath, pusher)
    pusher.addCollider(cNodePath, self.playerNode, base.drive.node())
  
  def update(self, dt):
    self.move(dt)    
  
  #Moves player
  def move(self, dt):
    #Change heading based on mouse movement
    mouse = base.win.getPointer(0) 
    x = mouse.getX() 
    y = mouse.getY() 
    if base.win.movePointer(0, base.win.getXSize()/2, base.win.getYSize()/2): 
      self.playerNode.setH(self.playerNode.getH() - (x - base.win.getXSize()/2)*.1)
      cam_p = base.camera.getP() - (y - base.win.getYSize()/2)*.1
      if cam_p >= -90 and cam_p <= 90:
        base.camera.setP(cam_p)
        
    self.pLightNode.setPos(0,self.lightDist*math.cos(deg2Rad(base.camera.getP())),
                           self.lightDist*math.sin(deg2Rad(base.camera.getP())))
    self.test.setPos(self.pLightNode.getPos())
    
    #Move player based on key movements
    if self.keyMap['forward'] == 1:
      self.playerNode.setPos(self.playerNode, self.forward * dt * self.speed)
    elif self.keyMap['back'] == 1:
      self.playerNode.setPos(self.playerNode, self.back * dt * self.speed)
    
    if self.keyMap['left'] == 1:
      self.playerNode.setPos(self.playerNode, self.left * dt * self.speed)
    elif self.keyMap['right'] == 1:
      self.playerNode.setPos(self.playerNode, self.right * dt * self.speed)
  
    