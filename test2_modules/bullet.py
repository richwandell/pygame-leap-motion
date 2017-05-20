from test2_modules.world_objects import Animateable, WorldObject
from collections import deque
import hashlib, time, math, random


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
    #max bullets to keep on the screen
    max_bullets = 50
    #object ids for a fifo queue of bullets
    bullet_queue = deque()
    #change in time from t0 to t
    dt = 0
    
    #gravity for the balls
    G = 0
            
    def calc(self):                                
        self.v = self.addVectors(self.v, self.G)
                                
        self.dx = self.v[0] * math.cos(self.v[1])
        
        self.dy = self.v[0] * math.sin(self.v[1])
                      
    def draw(self):                        
        self.move(x=self.dx, y=self.dy)
        self.checkScreenBounds()
        self.checkObjectColision()
        
        if self.y > self.stage.height - (20+self.m):
            self.setPosition((self.x, self.stage.height - (20+self.m)))
        
        
        
    def collisionHandler(self, colliders):        
        colliders = list(x for x in colliders if isinstance(x, Bullet))
        
        A = math.atan2(self.stage.mouse_y - self.stage.world_objects['cannon'].cannon_head[1], self.stage.mouse_x - self.stage.world_objects['cannon'].cannon_head[0])        
        
        
        for c in colliders:                      
            if self.y < c.y and self.x < c.x:
                A = math.atan2(c.y - self.y, c.x - self.x) % 360
                self.move(
                    x=(-self.m*2)*math.cos(A), 
                    y=(-self.m*2)*math.sin(A)
                )
                c.move(
                    x=(c.m*2)*math.cos(A),
                    y=(c.m*2)*math.sin(A)
                )
            elif self.y > c.y and self.x < c.x:
                A = math.atan2(self.y - c.y, self.x - c.x) % 360
                self.move(
                    x=(-self.m*2)*math.cos(A),
                    y=(self.m*2)*math.sin(A)
                )
                c.move(
                    x=(c.m*2)*math.cos(A),
                    y=(-c.m*2)*math.sin(A)
                )
            elif self.y < c.y and self.x > c.x:
                A = math.atan2(c.y - self.y, c.x - self.x) % 360
                self.move(
                    x=(self.m*2)*math.cos(A),
                    y=(-self.m*2)*math.sin(A)
                )
                c.move(
                    x=(-c.m*2)*math.cos(A),
                    y=(c.m*2)*math.sin(A)
                )
            else:
                A = math.atan2(self.y - c.y, self.x - c.x) % 360
            
            
            v1 = (self.v[0]*(self.m-c.m) + 2*c.m*c.v[0]) / (self.m + c.m)
            v2 = (c.v[0]*(c.m-self.m) + 2*self.m*self.v[0]) / (self.m+c.m)
            
            self.v = v1 , (self.v[1] - A)
            c.v = v2 , (c.v[1] - A)
        
        
    def boundsReachedHandler(self, side):      
        if side == "top":                
            self.v = self.v[0], math.radians(360) - self.v[1]
        elif side == "bottom":            
            self.v =self.v[0] - 1, math.radians(360) - self.v[1]
        elif side == "left" or side == "right":
            self.v = self.v[0], math.radians(180) - self.v[1]

        
    def __init__(self, position=(0,0), stage={}, velocity=(0,0)):
        
        self.m = random.randint(1, 10)
        
        #set initial acceleration
        self.v = velocity
        
        #set t0
        self.t0 = time.time()
                        
        self.G = (self.m * ((9.8*.08)**2), math.radians(90))                
        
        self.x, self.y = position
        
        self.can = stage.can
        self.stage = stage
        self.world_recursion = False
        
        xy = int(self.x - self.m), int(self.y - self.m), int(self.x + self.m), int(self.y + self.m)
        if len(Bullet.bullet_queue) > Bullet.max_bullets:
            b = Bullet.bullet_queue.popleft()
            self.cobj = b.cobj
            self.stage.can.coords(b.cobj, xy[0], xy[1], xy[2], xy[3])
        else:                       
            arc = self.stage.can.create_oval(xy, fill="red")
            self.cobj = arc
            
        self.object_id = str(self.cobj)
        self.stage.world_objects[self.object_id] = self
        Bullet.bullet_queue.append(self)
        self.calc()