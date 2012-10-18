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

class World(DirectObject): #necessary to accept events
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
    # available obstacle models
    obst_models = ("mushroom", "boulder")

    def __init__(self):
        #turn off default mouse control
        #otherwise we can't position the camera
        base.disableMouse()

        # per pixel lighting
        render.setShaderAuto()

        # load the models
        self.loadModels()

        # look at the penguin and position near it
        camera.lookAt(self.penguin)
        self.resetCamera()

        # set up the key dictionary
        self.keyMap = {"left":0, "right":0, "forward":0, "back":0}

        # set the previous time to 0, used to find dt for movement etc.
        self.prevTime = 0

        # set up the movement task
        taskMgr.add(self.move, "moveTask")
        
        # set up the collision objects
        self.setupCollisions()
        
        # set up the lights
        self.setupLights()

        # try and set up the particle effect
        self.setupParticles()

        # accept escape as the exit key
        self.accept("escape", sys.exit) #message name, function to call, (optional) list of arguments to that function
        
        #for "continuous" control
        map (self.accept \
            , self.defaultKeys \
            , (self.setKey for i in range(len(self.defaultKeys))) \
            , self.defaultArgs)
        
        #for secondary keys (wasd)
        map (self.accept \
            , self.defaultKeys2 \
            , (self.setKey for i in range(len(self.defaultKeys2))) \
            , self.defaultArgs)
    
    def setKey(self, key, value):
        self.keyMap[key] = value
        
    def loadModels(self):
        """loads initial models into the world"""
        # load the environment.  that lovely lovely plane.
        self.env = loader.loadModel("../assets/plane")
        self.env.reparentTo(render)
        self.env.setPos(0, 0, 0)

        # load the penguin, because rocketpenguin
        self.penguin = loader.loadModel("../assets/penguin")
        self.penguin.reparentTo(render)
        self.penguin.setH(180)

        # load the obstacles
        self.obstacles = [self.loadObstacle() for i in range(10)]

    def loadObstacle(self):
        # pick randomly, selecting a mushroom or a boulder
        obstacle = loader.loadModel(self.obst_models[random.randint(0,1)])

        # scale it down to half size...TODO make it the right size
        obstacle.setScale(.5)

        # set the obstacle position as some random spot on the plane
        obstacle.setPos(random.uniform(-80, 80), random.uniform(-80, 80), 0)

        # reparent to render
        obstacle.reparentTo(render)

        # return the obstacle
        return obstacle
        
    def setupLights(self):
        """loads initial lighting"""
        # try and load a cross-hatching shader
        #self.hatch_shader = Shader.load("../assets/shaders/Hatching.cg", Shader.SLCg)
        #self.hatch_shader.setShaderInput("eyePosition", camera_position_object_space)
        #self.hatch_shader.setShaderInput("worldviewproj", worldviewproj_matrix)
        #self.hatchShader.setShaderInput(
        # i have no idea what i'm doing here...asking for help from past years just got the response "why..why are you doing shaders in panda"
        
        # set up an ambient light
        self.ambientLight = AmbientLight("ambientLight")
        
        #for setting colors, alpha is largely irrelevant
        # slightly blue to try and produce a wintry, snowy look
        self.ambientLight.setColor((.04, .04, .05, 1.0))
        
        #create a NodePath, and attach it directly into the scene
        self.ambientLightNP = render.attachNewNode(self.ambientLight)
        
        #the node that calls setLight is what's illuminated by the given light
        #you can use clearLight() to turn it off
        render.setLight(self.ambientLightNP)
        
        # set up a directional light, sort of like the sun
        self.dirLight = DirectionalLight("dirLight")
        self.dirLight.setColor((.91, .9, .7, 1))
        self.dirLightNP = render.attachNewNode(self.dirLight)
        self.dirLightNP.setHpr(0, -25, 0)
        render.setLight(self.dirLightNP)

        # attempt to set light as shadow caster
        self.dirLight.setShadowCaster(True, 1024, 1024)
        render.setShaderAuto()

        # load the extra collision objects that mark where the light for the rocket is
        light_orig = self.penguin.find("**/lightOrigin")
        light_dir = self.penguin.find("**/lightDirection")
        self.rocketLight = Spotlight("rocket")
        self.rocketLight.setColor((.7, .5, .3, 1))
        self.rocketLight.setLens(PerspectiveLens())
        self.rNode = render.attachNewNode(self.rocketLight)
        self.rNode.setPos(light_orig.node().getSolid(0).getCollisionOrigin())
        self.rNode.setZ(8)
        light_target = light_dir.node().getSolid(0).getCollisionOrigin() + light_dir.getPos()
        self.rNode.lookAt(light_target.getX(), light_target.getY(), light_target.getZ())
        self.rNode.reparentTo(self.penguin)
        render.setLight(self.rNode)
        
    def move(self, task):
        """compound interval for walking"""
        dt = task.time - self.prevTime

        # have the camera turn to look at the model
        camera.lookAt(self.penguin)

        # setup if/where the penguin is moving
        if self.keyMap["left"] == 1:
            self.penguin.setH(self.penguin.getH() + dt*180) # turns 180 degrees a second
        if self.keyMap["right"] == 1:
            self.penguin.setH(self.penguin.getH() - dt*180)
        if self.keyMap["forward"] == 1:
            dist = 1 
            angle = deg2Rad(self.penguin.getH())
            dx = dist * math.sin(angle)
            dy = dist * -math.cos(angle)
            self.penguin.setPos(self.penguin.getX() + dx, self.penguin.getY() + dy, 10)
            self.resetCamera()
        if self.keyMap["back"] == 1:
            dist = 1
            angle = deg2Rad(self.penguin.getH())
            dx = dist * math.sin(angle)
            dy = dist * -math.cos(angle)
            self.penguin.setPos(self.penguin.getX() - dx, self.penguin.getY() - dy, 10)
            self.resetCamera()

        # reset the previous time
        self.prevTime = task.time

        # be sure that the penguin stays at z = 0
        self.penguin.setZ(12)
        self.env.setZ(-1)

        return Task.cont

    def resetCamera(self):
        # set the camera position and direction
        # get the vector between the penguin and camera
        cvec = self.penguin.getPos() - camera.getPos()
        # normalize it
        cvec.normalize()
        # get the change in camera position
        cdx = 80 * cvec[0]
        cdy = 80 * cvec[1]
        # find the new x and y for the camera
        cx = self.penguin.getX() - cdx
        cy = self.penguin.getY() - cdy
        # set the camera position
        camera.setPos(cx, cy, 20)

    def setupParticles(self):
        base.enableParticles()
        self.rFlame = ParticleEffect()
        self.rFlame.loadConfig("../assets/rockettest.ptf")
        self.rFlame.start(self.penguin)
        self.rFlame.setPos(0, 8, 8)

    def setupCollisions(self):
        #make a collision traverser, set it to default
        base.cTrav = CollisionTraverser()
        
        #make a pusher
        self.pusher = CollisionHandlerPusher()

        # make things to handle floor
        #fromObj = self.penguin.attachNewNode(CollisionNode('flrNode'))
        #fromObj.node().addSolid(CollisionRay(0, 0, 1, 0, 0, -1))

        #self.lifter = CollisionHandlerFloor()
        #self.lifter.addCollider(fromObj, self.penguin)
        #base.cTrav.addCollider(fromObj, self.lifter)
        
        #cSphere = CollisionSphere((0,0,0), 1) #penguin is scaled way down!
        #cNode = CollisionNode("penguin")
        cNode = self.loadColObj(self.penguin, "penguinSphere")
        #cNode.addSolid(cSphere)
        #penguin is *only* a from object
        cNode.node().setIntoCollideMask(BitMask32.allOff())
        #cNode.show()
        #cNodePath = self.penguin.attachNewNode(cNode)
        #base.cTrav.addCollider(cNodePath, self.cHandler)
        #self.pusher.addCollider(cNode, base.camera)
        # somehow making the penguin a from object and registering it
        #   with the pusher makes it push the ground plane up, even though
        #   the ground isn't a collision object...
        self.pusher.addCollider(cNode, self.penguin)
        base.cTrav.addCollider(cNode, self.pusher)
        self.penguin.setZ(12)

        #cnode = self.env.attachNewNode(CollisionNode('floorBox'))
        #cnode.node().addSolid(CollisionBox((0 - self.env.node().getBounds().getRadius(), 0 - self.env.node().getBounds().getRadius(), 0), (self.env.node().getBounds().getRadius() * 2, self.env.node().getBounds().getRadius() * 2, -10)))
        #cnode.setPos(0,0,0)
        self.env.setPos(0,0,0)
        #cnode.show()

        for obstacle in self.obstacles:
            #cSphere = CollisionSphere((0,0,0), 2)
            try:
                cNode = self.loadColObj(obstacle, "boulderCollide")
                #cNode.node().setIntoCollideMask()
                #cNode.show()
                #self.pusher.addCollider(cNode, obstacle)
                #base.cTrav.addCollider(cNode, self.pusher)
            except ValueError:
                try:
                    cNode = self.loadColObj(obstacle, "mushCollider")
                    #cNode.show()
                    #self.pusher.addCollider(cNode, obstacle)
                    #base.cTrav.addCollider(cNode, self.pusher)
                except ValueError as e:
                    print(e.args)
            #cNode = CollisionNode("mushroom")
            #cNode.addSolid(cSphere)
            #cNodePath = obstacle.attachNewNode(cNode)
            #cNodePath.show()

    def loadColObj(self, model, name):
        cNode = model.find("**/"+name)
        if cNode.getNumNodes() < 1:
            raise ValueError("Couldn't find " + name + " in " + model.getName())
        elif cNode.node().isGeomNode():
            raise ValueError(name + " is a geometry node!")
        else:
            collider = model.attachNewNode(CollisionNode(name))

            collider.setPos(cNode.getPos())
            collider.node().addSolid(cNode.node().getSolid(0))
            origin = cNode.node().getSolid(0).getCollisionOrigin()
            return collider
        
w = World()
run()
