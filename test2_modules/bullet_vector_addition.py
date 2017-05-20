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
    
    radius = 5
            
    def draw(self):
        if self.y > self.stage.height:
            self.theta = self.theta - 180
        elif self.y < 0:
            self.theta = self.theta + 180
        elif self.x > self.stage.width:
            if self.theta < 90:
                self.theta += 180
            else:
                self.theta -= 180
        elif self.x < 0:
            if self.theta > 180:
                self.theta -= 180
            else:
                self.theta += 180
        #self.checkObjectColision()
                    
                 
        (self.theta, self.speed) = self.addVectors((self.theta, self.speed), self.gravity) 
        self.x += (self.speed * math.cos(self.theta))
        self.y += (self.speed * math.sin(self.theta))
        
    
        
        self.stage.can.coords(self.cobj, self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius)
        
    def collisionHandler(self, coliders):
        c = coliders[0]
                
        
        dx = self.x - c.x            
        dy = self.y - c.y            
        distance = math.hypot(dx, dy)
        tangent = math.atan2(dy, dx)
        
        self.theta = 2*tangent - self.theta
        c.theta = 2*tangent - c.theta    
        (self.speed, c.speed) = (self.speed, c.speed)
            
        
        
    def __init__(self, theta=0, position=(0,0), stage={}, speed=0):
        
        self.theta = theta
        
        self.x, self.y = position
        
        #set initial velocity
        self.v0 = speed
        self.speed = speed                                                
        
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