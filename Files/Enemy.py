from pandac.PandaModules import * #basic Panda modules
from direct.showbase.DirectObject import DirectObject #event handling
from panda3d.ai import * #panda AI
import math, time

class Enemy(object):
  def __init__(self):
    self.speed = .03
    
    self.foundPlayer = False
    self.foundPlayerTime = -1
    
    base.accept("collide-vision", self.collideVision)
    
    self.initEnemy()
    self.initAI()
    
  #Loads player node, camera, and light
  def initEnemy(self):
    self.enemyNode = loader.loadModel('smiley')
    self.enemyNode.setPos(0,0,3)
    self.enemyNode.reparentTo(render)
    
  def initCollisions(self, cHandler, player):
      
    goodMask = BitMask32(0x1)
    badMask = BitMask32(0x2)
    otherMask = BitMask32(0x4)
    
    """
    cSphere = CollisionSphere( (0,0,0), 1.25 )
    cNode = CollisionNode('enemyPusher')
    cNode.addSolid(cSphere)
    cNode.setCollideMask(BitMask32(0x8))
    cNodePath = self.enemyNode.attachNewNode(cNode)
    base.pusher.addCollider(cNodePath, self.enemyNode)
    base.cTrav.addCollider(cNodePath, base.pusher)
    """
    
    cSphere = CollisionSphere( (0,0,0), 1.25 )
    cNode = CollisionNode('enemy')
    cNode.addSolid(cSphere)
    cNode.setIntoCollideMask(badMask)
    cNodePath = self.enemyNode.attachNewNode(cNode)
    #cNodePath.show()
    
    cTube = CollisionTube (0,-4,0,0,-6,0, 6)
    cNode = CollisionNode('vision')
    cNode.addSolid(cTube)
    cNodePath = self.enemyNode.attachNewNode(cNode)
    cNode.setIntoCollideMask(goodMask)
    #cNodePath.show()
    
    cRay = CollisionRay(self.enemyNode.getX(), self.enemyNode.getY(), self.enemyNode.getZ(), self.enemyNode.getX() - player.playerNode.getX(), self.enemyNode.getY() - player.playerNode.getY(), self.enemyNode.getZ() - player.playerNode.getZ())
    self.cNode = CollisionNode('sight')
    self.cNode.addSolid(cRay)
    self.cNode.setCollideMask(otherMask)
    cNodePath = self.enemyNode.attachNewNode(self.cNode)
    base.cTrav.addCollider(cNodePath, cHandler)
    #cNodePath.show()
    
  def initAI(self):
    self.AIworld = AIWorld(render)
 
    self.AIchar = AICharacter('enemyNode',self.enemyNode, 120, 0.05, 5)
    self.AIworld.addAiChar(self.AIchar)
    self.AIbehaviors = self.AIchar.getAiBehaviors()        

    #Path follow (note the order is reveresed)
    self.AIbehaviors.pathFollow(1.0)
    
    self.AIbehaviors.addToPath((0,10,3))
    self.AIbehaviors.addToPath((0,-10,3))
 
    self.AIbehaviors.startFollow()
    
  def update(self, dt, player):
    if self.AIchar.getVelocity() == LVecBase3f(0, 0, 0):
        self.AIbehaviors.startFollow()
    
    self.cNode.modifySolid(0).setOrigin(LPoint3f (self.enemyNode.getX(), self.enemyNode.getY(), self.enemyNode.getZ()))
    self.cNode.modifySolid(0).setDirection(LVector3f (self.enemyNode.getX() - player.playerNode.getX(), self.enemyNode.getY() - player.playerNode.getY(), self.enemyNode.getZ() - player.playerNode.getZ()))
    
    #after chasing for 5 seconds, goes back to the normal pattern
    if time.time() > self.foundPlayerTime + 5:
        self.foundPlayerTime = -1
        self.foundPlayer = False
    
    if self.foundPlayer == True:
        self.move(dt, player)
    else:
        self.AIworld.update()  
    
  #Moves player
  def move(self, dt, player):
    hypotenuse = math.sqrt( (player.playerNode.getX() - self.enemyNode.getX())**2 + (player.playerNode.getY() - self.enemyNode.getY())**2 ) 
    my_cos = (player.playerNode.getX() - self.enemyNode.getX()) / hypotenuse
    my_sin = (player.playerNode.getY() - self.enemyNode.getY()) / hypotenuse
    self.enemyNode.setPos(self.enemyNode.getX() + my_cos * self.speed, self.enemyNode.getY() + my_sin * self.speed, self.enemyNode.getZ())
    self.enemyNode.lookAt(player.playerNode)
    self.enemyNode.setH(self.enemyNode.getH() - 180)
    
    if hypotenuse < 10.0:
        self.foundPlayerTime = time.time()
        self.foundPlayer = True
    
  def collideVision(self, cEntry):
    if self.foundPlayer == False:
        self.foundPlayerTime = time.time()
        self.foundPlayer = True
    