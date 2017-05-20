from test2_modules.world_objects import Animateable, WorldObject
from collections import deque
import hashlib, time, math

class Bullet(Animateable, WorldObject):
    """
    Bullet object inherit from animateable and world object objects. 
    Bullets will be given an initial tradjectory, position, and velocity
    The velocity will decrease with the acceleration of 10 pixels / 100 millisecond
    """
    #mass
    m = 5
    #initial time 
    t0 = 0            
    #x initial
    x0 = 0
    #y initial
    y0 = 0
    #velocity in the x direction    
    vx = 0
    #velocity in the y direction
    vy = 0
    ax = 0
    ay = 0
    #the angle
    theta = 0        
    #The potential energy
    Ep = 0
    #The current kinetic energy
    Ek = 0        
    #max bullets to keep on the screen
    max_bullets = 500
    #object ids for a fifo queue of bullets
    bullet_queue = deque()
    #change in time from t0 to t
    dt = 0
    #whether or not this object has gravity
    has_gravity = True        
            
    def draw(self):            
        if self.y > self.stage.height - 20:
            self.move(y=-20)
            self.t0 = time.time()     
            self.v0 = self.v0 - 5      
            
        self.dt = time.time() - self.t0

        self.vx = self.v0
        self.vy = self.v0 + (self.m * -9.8 * self.dt)
        
        dt = self.dt
        if dt == 0:
            self.ax = 0 
            self.ay = 0
        else:
            self.ax = (self.vx*math.cos(self.theta) - self.v0x) / self.dt 
            self.ay = (self.vy*math.sin(self.theta) - self.v0y)/ self.dt
        
        #kinetic energy = 1/2 mv^2
        self.Ek = .5 * Bullet.m * self.vy**2
                        
        #change in x is velocity times cos(theta)
        dx = self.vx * math.cos(self.theta)
        #change in y is velocity times sin(theta)
        dy = self.vy * math.sin(self.theta)                        
        
        self.move(x = dx, y = dy)
        
    def collisionHandler(self, coliders):
        #TODO Not sure how to handle this part yet
        pass
#        for c in coliders:
#            if c.x < self.x:
#                xmove = c.x - self.ax / 50
#            else:
#                xmove = c.x + self.ax / 50
#            if c.y > self.y:
#                ymove = c.y + self.ay / 50
#            else:
#                ymove = c.y - self.ay / 50
#            c.setPosition((xmove, ymove))
            
        
        
    def __init__(self, theta=0, position=(0,0), stage={}, velocity=0):
        
        #set initial velocity
        self.v0 = velocity
        
        #set initial x velocity
        self.v0x = velocity * math.cos(theta)
        #set initial y velocity
        self.v0y = velocity * math.sin(theta)
        
        #set x and x initial
        self.x = position[0]
        self.x0 = position[0]
        
        #set y and y initial
        self.y = position[1]
        self.y0 = position[1]
        
        #set theta
        self.theta = theta / 5
        
        #set t0
        self.t0 = time.time()
        
        #potential energy = mgh
        self.Ep = self.m * 9.8 * self.y
        
        
        self.can = stage.can
        self.stage = stage
        self.world_recursion = False
                                        
        xy = int(self.x - 5), int(self.y - 5), int(self.x + 5), int(self.y + 5)
        arc = self.stage.can.create_oval(xy, fill="red")
        
        self.cobj = arc
        self.object_id = hashlib.md5(str(self.cobj)).hexdigest()                
        self.stage.world_objects[self.object_id] = self
        Bullet.bullet_queue.append(self)