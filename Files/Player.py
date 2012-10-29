from pandac.PandaModules import * #basic Panda modules
from direct.showbase.DirectObject import DirectObject #event handling
import math
from Files.HUD import *
from direct.particles.ParticleEffect import ParticleEffect #particle effects

class Movement(object):
  def __init__(self, speed, bobSpd, bobAmt):
    self.speed = speed
    self.bobSpd = bobSpd
    self.bobAmt = bobAmt

class Player(object):
  #Initializes player
  def __init__(self):
    #Movement data
    self.speed = 40
    self.playerScale = 0.05
    self.lightDist = 0.1
    self.movement = {}
    self.movement['stand'] = Movement(0, 0.03, 1.3)
    self.movement['caution'] = Movement(1, 0.051, 2.1)
    self.movement['walk'] = Movement(1.5, 0.079, 2.7)
    self.movement['sprint'] = Movement(4, 0.16, 3.6)
    self.forward = Vec3(0,1,0)
    self.back = Vec3(0,-1,0)
    self.left = Vec3(-1,0,0)
    self.right = Vec3(1,0,0)
    self.bobTimer = 0
    self.recharging = True
    self.energyLeft = 100
    self.maxEnergy = 100
    #Ability data
    self.itemNode = NodePath('item')
    self.itemLoaded = False
    self.itemMax = 6
    self.itemDist = self.itemMax
    self.sideBuffer = 0
    self.wallModel = loader.loadModel('Models/WallTemp')
    self.lightModel = loader.loadModel('Models/light')
    self.lights = []
    self.lightZ = 2
    self.wallsLeft = 3
    self.lightsLeft = 3
    self.cRay1 = None
    self.cRay2 = None
    self.cRay3 = None
    #HUD
    self.hud = HUD(self.wallsLeft, self.lightsLeft)
    
    self.timer = 0
        
    self.initKeyMap()
    self.initControls()
    self.initPlayer()
    base.enableParticles()
    
  def respawn(self):
    print 'died'
    self.wallsLeft = 3
    self.lightsLeft = 3
    self.energyLeft = 100
    self.bobTimer = 0
    self.playerNode.setPos(-10,-10,3)
    
  #Initializes keyMap
  def initKeyMap(self):
    self.keyMap = {}
    self.keyMap['forward'] = 0
    self.keyMap['left'] = 0
    self.keyMap['right'] = 0
    self.keyMap['back'] = 0
    self.keyMap['sprint'] = 0
    self.keyMap['caution'] = 0
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
    base.accept('control', self.setKey, ['caution', 1])
    base.accept('control-up', self.setKey, ['caution', 0])
    base.accept('1', self.toggleKey, ['wall'])
    base.accept('2', self.toggleKey, ['light'])
    base.accept('f', self.cancelKey)
    base.accept('mouse1', self.click)
        
  #Sets key values
  def setKey(self, key, value):
    if key == 'sprint' and self.energyLeft <= 0:
      self.keyMap['sprint'] = 0
      return
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
      if ((key == 'wall' and self.wallsLeft > 0) or
        (key == 'light' and self.lightsLeft > 0)):
        self.loadItem(key)
    else:
      self.unloadItem(key)
      
  #Loads passed item
  def loadItem(self, item):
    #Clears and resets itemNode to toggled ability
    self.itemNode.detachNode()
    if item == 'wall':
      self.itemNode = self.wallModel
      self.itemNode.setColor(Vec4(1,1,1,0))
      self.itemNode.setScale(5)
      self.itemNode.setCollideMask(BitMask32.allOff())
    elif item == 'light':
      self.itemNode = self.lightModel
      self.itemNode.setColor(Vec4(1,1,1,1))
      self.itemNode.setScale(1.6)
    self.itemNode.reparentTo(self.playerNode)
    self.itemLoaded = True
    
    #Attach collisionRays to prevent items from going into env
    self.cRay1.reparentTo(base.camera)
    self.cRay2.reparentTo(base.camera)
    self.cRay3.reparentTo(base.camera)
    base.itemTrav.addCollider(self.cRay1, base.queue)
    base.itemTrav.addCollider(self.cRay2, base.queue)
    base.itemTrav.addCollider(self.cRay3, base.queue)
    
  #Removes item when toggled off
  def unloadItem(self, item):
    self.itemLoaded = False
    self.abilities[item] = 0
    self.itemNode.detachNode()
    self.cRay1.detachNode()
    self.cRay2.detachNode()
    self.cRay3.detachNode()
    
  #Cancels ability
  def cancelKey(self):
    for ability in self.abilities.keys():
      self.abilities[ability] = 0
    self.itemLoaded = False
    self.itemNode.detachNode()
    self.cRay1.detachNode()
    self.cRay2.detachNode()
    self.cRay3.detachNode()
    
  #Place item when clicked, then clear loaded item
  def click(self):
    if self.itemLoaded:
      self.placeItem()
      self.cancelKey()
  def placeItem(self):
    if self.abilities['wall'] == 1:
      self.placeWall()
      self.wallsLeft -= 1
    elif self.abilities['light'] == 1:
      self.placeLight()
      self.lightsLeft -= 1
    #Update HUD when ability is used
    self.hud.updateHUD(self.wallsLeft, self.lightsLeft)
  
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
    light = loader.loadModel('Models/light')
    #Adds emission material to placed light
    mat = Material()
    mat.setEmission(VBase4(0.2,0.2,0.45,1))
    light.setMaterial(mat)
    light.reparentTo(item)
    light.setScale(self.playerScale*1.6)
    #Attach point light to light ability item
    iLightNode = NodePath('ilight')
    iLightNode.reparentTo(item)
    iLightNode.setZ(iLightNode.getZ() + 0.5)
    iLight = PointLight('item-light')
    iLightNP = iLightNode.attachNewNode(iLight)
    iLightNP.node().setColor(Vec4(0.1, 0.15, 0.2, 1.0))
    iLightNP.node().setAttenuation(Vec3(0, 0.008, 0.0001))
    iLightNP.setZ(iLightNP.getZ() + 0.6)
    #Not for light ability?
    # particle effects
    rFlame = ParticleEffect()
    rFlame.loadConfig("Models/fire.ptf")
    rFlame.start(item)
    rFlame.setScale(0.1)
    pos = iLightNP.getPos()
    #rFlame.setPos(pos[0], pos[1], pos[2] + 0.4)
    rFlame.setPos(pos[0], pos[1], pos[2] - 0.2)
    render.setLight(iLightNP)
    #Sets placement time for rotating
    item.setTag('startTime', '%f' % self.timer)
    self.lights.append(item)
      
  def setPlayerPos(self, pos):
    self.playerNode.setPos(pos)

  #Loads player node, camera, and light
  def initPlayer(self):
    self.playerNode = NodePath('player-node')
    #setPos depends on spawn position in level
    self.playerNode.setPos(-10,-10,3)
    self.playerNode.setP(0)
    self.playerNode.setScale(self.playerScale)
    self.playerNode.reparentTo(render)
    
    #Loads camera
    lens =  base.cam.node().getLens()
    lens.setFov(90)
    base.cam.node().setLens(lens)
    base.camera.reparentTo(self.playerNode)
    
    #Loads hand
    hand = loader.loadModel('Models/hand')
    hand.reparentTo(base.camera)
    hand.setScale(0.8)
    hand.setPos(7,9,-9)
    hand.setH(90)
    ambientLight = AmbientLight("ambientLight")
    ambientLight.setColor((0.1, 0.1, 0.1, 1.0))
    ambientLightNP = render.attachNewNode(ambientLight)
    hand.setLight(ambientLightNP)
    
    #Loads artifact point light
    mat = Material()
    mat.setEmission(VBase4(0.2,0.2,0.45,1))
    self.test = loader.loadModel('Models/light')
    self.test.setMaterial(mat)
    self.test.reparentTo(base.camera)
    self.test.setScale(0.03)
    self.test.setPos(Vec3(1.4,1.6,-0.5))
    self.pLightNode = NodePath('light-node')
    self.pLightNode.reparentTo(base.camera)
    self.pLightNode.setPos(Vec3(1.33,2.4,0))
    pLight = PointLight('player-light')
    pLightNP = self.pLightNode.attachNewNode(pLight)
    pLightNP.node().setColor(Vec4(0.1, 0.15, 0.2, 1.0))
    pLightNP.node().setAttenuation(Vec3(0, 0.01, 0.0001))
    render.setLight(pLightNP)
    
  #Initialize collisions
  def initCollisions(self):
    envMask = BitMask32(0x1)
    sightMask = BitMask32(0x2)
    deathMask = BitMask32(0x3)
    clearSightMask = BitMask32(0x4)
    
    #Collide with enemies    
    cSphere = CollisionSphere( 0, 0, 2, 3 )
    cNode = CollisionNode('player')
    cNode.addSolid(cSphere)
    cNode.setCollideMask(BitMask32.allOff())
    cNodePath = self.playerNode.attachNewNode(cNode)
    #cNodePath.show()
    base.cTrav.addCollider(cNodePath, base.queue)
    
    #collide with enemy sight
    cSphere = CollisionSphere( 0, 0, 2, 3 )
    cNode = CollisionNode('playerSight')
    cNode.addSolid(cSphere)
    cNode.setCollideMask(BitMask32.allOff())
    cNode.setFromCollideMask(sightMask)
    cNode.setIntoCollideMask(clearSightMask)
    cNodePath = self.playerNode.attachNewNode(cNode)
    base.cTrav.addCollider(cNodePath, base.cHandler)
    
    #Collide with env
    cSphere = CollisionSphere(0,0,-2/self.playerScale,0.9/self.playerScale)
    cNode = CollisionNode('pusherNode')
    cNode.addSolid(cSphere)
    cNode.setCollideMask(envMask)
    cNodePath = self.playerNode.attachNewNode(cNode)
    #cNodePath.show()
    base.cTrav.addCollider(cNodePath, base.pusher)
    base.pusher.addCollider(cNodePath, self.playerNode, base.drive.node())
        
    #Item placement collision rays
    cNode = CollisionNode('rayRight')
    cRay = CollisionRay(0,0,0,0.4,1,0)
    cNode.addSolid(cRay)
    cNode.setCollideMask(BitMask32.allOff())
    cNode.setFromCollideMask(envMask)
    self.cRay1 = base.camera.attachNewNode(cNode)
    cNode = CollisionNode('rayLeft')
    cRay = CollisionRay(0,0,0,-0.4,1,0)
    cNode.addSolid(cRay)
    cNode.setCollideMask(BitMask32.allOff())
    cNode.setFromCollideMask(envMask)
    self.cRay2 = base.camera.attachNewNode(cNode)
    cNode = CollisionNode('rayMid')
    cRay = CollisionRay(0,0,0,0,1,0)
    cNode.addSolid(cRay)
    cNode.setCollideMask(BitMask32.allOff())
    cNode.setFromCollideMask(envMask)
    self.cRay3 = base.camera.attachNewNode(cNode)
    
    base.accept('enemy-into-player', self.respawn)
  
  #Updates player
  def update(self, dt):
    self.moveCam()
    self.movePlayer(dt)
    self.moveLight()
    if self.itemLoaded:
      self.itemRay()
    self.hud.updateEnergy(self.energyLeft)
    self.timer += 0.05
  
  def itemRay(self):
    base.itemTrav.traverse(render)
    base.queue.sortEntries()
    playerPos = base.camera.getPos(render)
    first = base.queue.getEntry(0)
    cPos = first.getSurfacePoint(render)
    rayName = first.getFromNodePath().getName()
    dist = math.sqrt((playerPos[0]-cPos[0])**2 + (playerPos[1]-cPos[1])**2)
    self.itemDist = min(dist, self.itemMax)
    """
    if rayName == 'rayLeft':
      self.sideBuffer = 0.5
    elif rayName == 'rayRight':
      self.sideBuffer = -0.5
    else:
      self.sideBuffer = 0
    """
  
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
    base.camera.setP(0)
    itemDist = max(self.itemDist-0.5,1)
    if self.abilities['light'] == 1:
      pos = Vec3(self.sideBuffer/self.playerScale,itemDist/self.playerScale, 
        (-1*self.playerNode.getZ()+self.lightZ)/self.playerScale)
    else:
      pos = Vec3(self.sideBuffer/self.playerScale,itemDist/self.playerScale,
        -1*self.playerNode.getZ()/self.playerScale)
    
    self.itemNode.setFluidPos(pos)
    
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
    self.recharging = True
    #Not moving
    if (self.keyMap['forward'] + self.keyMap['back'] +
        self.keyMap['left'] + self.keyMap['right']) == 0:
      move = self.movement['stand']
    #Moving
    elif self.keyMap['sprint'] and self.keyMap['forward'] == 1:
      move = self.movement['sprint']
      if self.energyLeft <= 0:
        self.energyLeft = 0
        self.keyMap['sprint'] = 0
      else:
        self.energyLeft -= 0.3
        self.recharging = False
    elif self.keyMap['caution'] == 1:
      move = self.movement['caution']
    else:
      move = self.movement['walk']
    
    if self.keyMap['forward'] == 1:
      self.playerNode.setPos(self.playerNode, self.forward * dt * move.speed * self.speed)
    elif self.keyMap['back'] == 1:
      self.playerNode.setPos(self.playerNode, self.back * dt * move.speed * self.speed)
    
    if self.keyMap['left'] == 1:
      self.playerNode.setPos(self.playerNode, self.left * dt * move.speed * self.speed)
    elif self.keyMap['right'] == 1:
      self.playerNode.setPos(self.playerNode, self.right * dt * move.speed * self.speed)
      
    self.headBob(move)
    if self.recharging and self.energyLeft < 100:
      self.energyLeft += 0.035
      
  
  def headBob(self, movement):
    waveslice = math.sin(self.bobTimer)
    if waveslice != 0:
      change = waveslice * movement.bobAmt
      base.camera.setZ(change)
    else:
      base.camera.setZ(0)
    self.bobTimer = (self.bobTimer + movement.bobSpd) % (math.pi*2)
    
  def moveLight(self):
    waveslice = math.sin(self.timer)
    for light in self.lights:
      change = waveslice * 0.1
      light.setZ( self.lightZ + change )
      light.setH((float(light.getTag('startTime')) + self.timer) * 8 )
    self.test.setZ( waveslice * 0.1 - 0.5)
    self.test.setH( self.timer * 4 )
