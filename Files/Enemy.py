from pandac.PandaModules import * #basic Panda modules
from direct.showbase.DirectObject import DirectObject #event handling
from panda3d.ai import * #panda AI
import math, time

class Enemy(object):
  def __init__(self, spawnPos, AIpath):
    self.speed = .03
    
    self.sightBlocked = True
    self.foundPlayer = False
    self.foundPlayerTime = -1
    self.spawnPos = spawnPos
    
    self.initEnemy()
    self.initAI(AIpath)
    
  #Loads player node, camera, and light
  def initEnemy(self):
    self.enemyNode = loader.loadModel('smiley')
    self.enemyNode.setPos(self.spawnPos)
    self.enemyNode.setScale(0.5)
    self.enemyNode.reparentTo(render)
    
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
    
  def initCollisions(self, player):
    envMask = BitMask32(0x1)
    sightMask = BitMask32(0x2)
    deathMask = BitMask32(0x3)
    clearSightMask = BitMask32(0x4)
    
    #collides with walls
    cSphere = CollisionSphere( (0,0,0), 1.25 )
    cNode = CollisionNode('enemyPusher')
    cNode.addSolid(cSphere)
    cNode.setCollideMask(BitMask32.allOff())
    cNode.setFromCollideMask(envMask)
    cNodePath = self.enemyNode.attachNewNode(cNode)
    base.pusher.addCollider(cNodePath, self.enemyNode)
    base.cTrav.addCollider(cNodePath, base.pusher)
    
    #collides with the player
    cSphere = CollisionSphere( (0,0,0), 1.5 )
    cNode = CollisionNode('enemy')
    cNode.addSolid(cSphere)
    cNode.setCollideMask(BitMask32.allOff())
    cNode.setFromCollideMask(deathMask)
    cNodePath = self.enemyNode.attachNewNode(cNode)
    cNodePath.show()
    base.cTrav.addCollider(cNodePath, base.cHandler)
    
    #collides with the player to determine if the player is in the enemie's cone of vision
    cTube = CollisionTube (0,-4,0,0,-6,0, 6)
    cNode = CollisionNode('vision')
    cNode.addSolid(cTube)
    cNode.setCollideMask(BitMask32.allOff())
    cNode.setIntoCollideMask(sightMask)
    cNodePath = self.enemyNode.attachNewNode(cNode)
    #cNodePath.show()
    
    #checks to see if there is anything blocking the enemie's line of sight to the player
    self.queue = CollisionHandlerQueue()
    cRay = CollisionRay(self.enemyNode.getX(), self.enemyNode.getY(), self.enemyNode.getZ(), self.enemyNode.getX() - player.playerNode.getX(), self.enemyNode.getY() - player.playerNode.getY(), self.enemyNode.getZ() - player.playerNode.getZ())
    self.cNode = CollisionNode('sight')
    self.cNode.addSolid(cRay)
    self.cNode.setCollideMask(BitMask32.allOff())
    self.cNode.setFromCollideMask(envMask|clearSightMask)
    cNodePath = base.render.attachNewNode(self.cNode)
    base.cTrav.addCollider(cNodePath, self.queue)
    
    base.accept('playerSight-again-vision', self.inSight)
    
  def inSight(self, cEntry):
    #print 'seen'
    if not self.foundPlayer and not self.sightBlocked:
      #print 'found'
      self.foundPlayer = True
      self.foundPlayerTime = time.time()
    if time.time() > self.foundPlayerTime + 5:
      self.foundPlayerTime -= 1
      self.foundPlayer = False
    
  def update(self, dt, player):
    if self.AIchar.getVelocity() == LVecBase3f(0, 0, 0):
        self.AIbehaviors.startFollow()
    
    #updates the enemie's vision ray towards the player
    self.cNode.modifySolid(0).setOrigin(LPoint3f (self.enemyNode.getX(), self.enemyNode.getY(), self.enemyNode.getZ()))
    self.cNode.modifySolid(0).setDirection(LVector3f ((self.enemyNode.getX() - player.playerNode.getX()) * -1, (self.enemyNode.getY() - player.playerNode.getY()) * -1, 0))
    
    #checks the first element that the enemy sees between the player
    #if the first object it sees is not the player then it doesn't chase towards it
    self.queue.sortEntries()
    #print self.queue
    if self.queue.getNumEntries() > 0:
        entry = self.queue.getEntry(0)
        type = entry.getIntoNode().getName()
        if type == 'playerSight':
            self.sightBlocked = False
            #print 'in sight'
        else:
            self.sightBlocked = True
            #print 'not in sight'
    
    """
    #checks to see if the player is in the enemie's vision cone and not blocked
    for i in range(base.eQueue.getNumEntries()):
        if base.eQueue.getEntry(i).getIntoNode().getName() == 'vision' and self.foundPlayer == False and self.sightBlocked == False:
            self.foundPlayer = True
            self.foundPlayerTime = time.time()
        
    #after chasing for 5 seconds, goes back to the normal pattern
    if time.time() > self.foundPlayerTime + 5:
        self.foundPlayerTime = -1
        self.foundPlayer = False
    """
    
    #if the player is found then moves towards them
    #otherwise continues patrolling
    if self.foundPlayer:
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
    
    #if the enemy is near enough to the player, it will keep looking
    if hypotenuse < 5.0 and self.sightBlocked == False:
        self.foundPlayerTime = time.time()
        self.foundPlayer = True
        
