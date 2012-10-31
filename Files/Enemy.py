from pandac.PandaModules import * #basic Panda modules
from direct.showbase.DirectObject import DirectObject #event handling
from panda3d.ai import * #panda AI
from direct.actor.Actor import Actor
import math, time

class Enemy(object):
  def __init__(self, parent, spawnPos, AIpath):
    self.speed = .1
    
    self.sightBlocked = False
    self.foundPlayer = False
    self.foundPlayerTime = -1
    self.spawnPos = spawnPos
    self.spawnH = 0
    
    self.parent = parent
    
    self.startH = -1
    self.blocked = False
    self.justUnblocked = False
    self.timeUnblocked = -1
    
    self.initEnemy()
    self.initSounds()
    self.initAI(AIpath)
    
  #Loads player node, camera, and light
  def initEnemy(self):
    self.enemyNode = Actor('Models/monster', {'walk':'Models/monsterWalkAnim',
                                              'run':'Models/monsterRunAnim'})
    self.enemyNode.reparentTo(render)
    self.enemyNode.setScale(0.2)
    self.enemyNode.setPos(self.spawnPos)
    self.enemyNode.setPlayRate(1.2, 'walk')
    self.enemyNode.loop('walk')
    
  def initSounds(self):
    self.stompSfx = base.loadSfx('sounds/stomp.ogg')
    self.stompSfx.setLoopCount(0)
    self.stompSfx.setVolume(.15)
    #self.chaseSfx = base.loadSfx('Sounds/chase.wav')
    #self.chaseSfx.setLoopCount(0)
    self.movementSfx = None
    
  #AIpath is a list of vertices
  def initAI(self, AIpath):
    
    self.AIworld = AIWorld(render)
    
    self.AIchar = AICharacter('enemyNode',self.enemyNode, 120, 0.05, 5)
    
    self.AIworld.addAiChar(self.AIchar)
    self.AIbehaviors = self.AIchar.getAiBehaviors()        
    #Path follow (note the order is reveresed)
    self.AIbehaviors.pathFollow(1.0)
    
    for point in AIpath:
      self.AIbehaviors.addToPath(point)
 
    self.AIbehaviors.startFollow()
   
  def respawn(self):
    self.enemyNode.setPos(self.spawnPos)
    self.enemyNode.setH(self.spawnH)
    self.foundPlayer = False
    
  def initCollisions(self, player):
    envMask = BitMask32(0x1)
    sightMask = BitMask32(0x2)
    deathMask = BitMask32(0x4)
    clearSightMask = BitMask32(0x8)
    
    #collides with walls
    cSphere = CollisionSphere( (0,0,20), 10)
    cNode = CollisionNode('enemyPusher')
    cNode.addSolid(cSphere)
    cNode.setCollideMask(BitMask32.allOff())
    cNode.setFromCollideMask(envMask)
    cNodePath = self.enemyNode.attachNewNode(cNode)
    base.pusher.addCollider(cNodePath, self.enemyNode)
    base.cTrav.addCollider(cNodePath, base.pusher)
    #cNodePath.show()
    
    #collides with the player
    cSphere = CollisionSphere( (0,0,20), 20 )
    cNode = CollisionNode('enemy')
    cNode.addSolid(cSphere)
    cNode.setCollideMask(BitMask32.allOff())
    cNode.setFromCollideMask(deathMask)
    cNodePath = self.enemyNode.attachNewNode(cNode)
    base.cTrav.addCollider(cNodePath, base.cHandler)
    #cNodePath.show()
    
    #collides with the player to determine if the player is in the enemie's cone of vision
    cTube = CollisionTube (0,-40,0,0,-60,0, 60)
    cNode = CollisionNode('vision')
    cNode.addSolid(cTube)
    cNode.setCollideMask(BitMask32.allOff())
    cNode.setIntoCollideMask(sightMask)
    cNodePath = self.enemyNode.attachNewNode(cNode)
    #cNodePath.show()
    
    #checks to see if there is anything blocking the enemie's line of sight to the player
    self.queue = CollisionHandlerQueue()
    cRay = CollisionRay(self.enemyNode.getX(), self.enemyNode.getY(), self.enemyNode.getZ() + 5, self.enemyNode.getX() - player.playerNode.getX(), self.enemyNode.getY() - player.playerNode.getY(), self.enemyNode.getZ() - player.playerNode.getZ())
    self.cNode = CollisionNode('sight')
    self.cNode.addSolid(cRay)
    self.cNode.setCollideMask(BitMask32.allOff())
    self.cNode.setFromCollideMask(envMask|clearSightMask)
    cNodePath = base.render.attachNewNode(self.cNode)
    base.cTrav.addCollider(cNodePath, self.queue)
    #cNodePath.show()
    
    #checks to see if it is blocked by a wall while patrolling
    self.wallQueue = CollisionHandlerQueue()
    cRay = CollisionRay(2, 0, 10, 0, -1, 0)
    cNode = CollisionNode('wallSight')
    cNode.addSolid(cRay)
    cNode.setCollideMask(BitMask32.allOff())
    cNode.setFromCollideMask(envMask|clearSightMask)
    cNodePath = self.enemyNode.attachNewNode(cNode)
    base.cTrav.addCollider(cNodePath, self.wallQueue)
    #cNodePath.show()
    
    base.accept('playerSight-again-vision', self.inSight)
    
  def inSight(self, cEntry):
    if not self.foundPlayer and not self.sightBlocked:
      self.foundPlayer = True
      self.foundPlayerTime = time.time()
      #self.enemyNode.loop('run')
    
  def update(self, dt, player):
    if self.AIchar.getVelocity() == LVecBase3f(0, 0, 0):
        self.AIbehaviors.startFollow()
    
    #updates the enemie's vision ray towards the player
    self.cNode.modifySolid(0).setOrigin(LPoint3f (self.enemyNode.getX(), self.enemyNode.getY(), self.enemyNode.getZ() + 5))
    self.cNode.modifySolid(0).setDirection(LVector3f ((self.enemyNode.getX() - player.playerNode.getX()) * -1, (self.enemyNode.getY() - player.playerNode.getY()) * -1, 0))
    
    self.wallQueue.sortEntries()
    wallSearch = True
    wallSearchIndex = 0
    while wallSearch == True:
        if self.wallQueue.getNumEntries() > 0 and wallSearchIndex < self.wallQueue.getNumEntries():
            entry = self.wallQueue.getEntry(wallSearchIndex)
            type = entry.getIntoNode().getName()
            
            if type == 'start' or type == 'exit' or ('enemy' in type and type != 'enemyPusher'):
                wallSearchIndex = wallSearchIndex + 1
                continue
                
            wallSearch = False
            
            if type == 'Wall':
                if self.blocked == False:
                    self.startH = self.enemyNode.getH()
                self.blocked = True
            else:
                self.blocked = False
                self.justUnblocked = True
                self.timeUnblocked = time.time()
        else:
            wallSearch = False
            if self.blocked == True:
                self.blocked = False
                self.justUnblocked = True
                self.timeUnblocked = time.time()
            
    #checks the first element that the enemy sees between the player
    #if the first object it sees is not the player then it doesn't chase towards it
    self.queue.sortEntries()
    sightSearch = True
    sightSearchIndex = 0
    while sightSearch == True:
        if self.queue.getNumEntries() > 0 and sightSearchIndex < self.queue.getNumEntries():
            entry = self.queue.getEntry(sightSearchIndex)
            type = entry.getIntoNode().getName()
            
            if type == 'start' or type == 'exit' or ('enemy' in type and type != 'enemyPusher'):
                sightSearchIndex = sightSearchIndex + 1
                continue
            
            sightSearch = False
            
            if type == 'playerSight':
                self.sightBlocked = False
            else:
                self.sightBlocked = True
        else:
            sightSearch = False
        
    #if the player is found then moves towards them
    #otherwise continues patrolling
    if self.foundPlayer:
        self.move(dt, player)
        self.parent.chaseBGM(True)
    else:
        self.parent.chaseBGM(False)
        if self.blocked == True:
            self.enemyNode.setH(self.enemyNode.getH() - 15)
        elif self.justUnblocked == True:
            if self.timeUnblocked + 3.0 < time.time():
                self.justUnblocked = False
                self.timeUnblocked = -1
            else:
                x_adjustment = 1
                y_adjustment = 1

                measure_against = self.startH % 360
                if self.enemyNode.getH() < 0:
                    measure_against = 360 - measure_against
                    
                if measure_against >=0 and measure_against < 90:
                    x_adjustment = 1
                    y_adjustment = -1
                if measure_against >=90 and measure_against < 180:
                    x_adjustment = 1
                    y_adjustment = 1
                if measure_against >= 180 and measure_against < 270:
                    x_adjustment = -1    
                    y_adjustment = 1
                if measure_against >= 270 and measure_against < 360:
                    x_adjustment = -1
                    y_adjustment = -1
                    
                angle = self.startH - self.enemyNode.getH()
                self.enemyNode.setX(self.enemyNode.getX() + x_adjustment * math.fabs(math.sin(math.radians(angle))) * self.speed)
                self.enemyNode.setY(self.enemyNode.getY() + y_adjustment * math.fabs(math.cos(math.radians(angle))) * self.speed)
        else:
            self.AIworld.update()  
            
    if time.time() > self.foundPlayerTime + 5:
      self.foundPlayer = False
      
    #Movement SFX
    #if self.foundPlayer and self.movementSfx != self.chaseSfx:
    #  if self.movementSfx != None:
    #    self.movementSfx.stop()
    #  self.movementSfx = self.chaseSfx
    #  self.movementSfx.play()
    #if not self.foundPlayer and self.movementSfx != self.stompSfx:
    if self.movementSfx != self.stompSfx:
        if self.movementSfx != None:
          self.movementSfx.stop()
        self.movementSfx = self.stompSfx
        self.movementSfx.play()
    
  #Moves player
  def move(self, dt, player):
    hypotenuse = math.sqrt( (player.playerNode.getX() - self.enemyNode.getX())**2 + (player.playerNode.getY() - self.enemyNode.getY())**2 ) 
    my_cos = (player.playerNode.getX() - self.enemyNode.getX()) / hypotenuse
    my_sin = (player.playerNode.getY() - self.enemyNode.getY()) / hypotenuse
    self.enemyNode.setPos(self.enemyNode.getX() + my_cos * self.speed, self.enemyNode.getY() + my_sin * self.speed, self.enemyNode.getZ())
    self.enemyNode.lookAt(player.playerNode.getX(), player.playerNode.getY(), self.enemyNode.getZ())
    self.enemyNode.setH(self.enemyNode.getH() - 180)
    
    #if the enemy is near enough to the player, it will keep looking
    if hypotenuse < 5.0 and self.sightBlocked == False:
        self.foundPlayerTime = time.time()
        self.foundPlayer = True
        
