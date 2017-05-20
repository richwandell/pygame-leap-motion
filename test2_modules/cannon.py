import math
from test2_modules.world_objects import Animateable, WorldObject

class Cannon(Animateable, WorldObject):
    """
    Cannons have a arc body and a cannon arm that moves around with the 
    mouse movement
    
    cannon_head is the coordinates of the tip of the cannon arm this is used for 
    bullets that come out of the cannon
    
    cannon_angle is used for calculating the trajectory of the bullets that are 
    fired out of the cannon
    """
    #tip of the cannon
    cannon_head = 0, 0
    #cannon angle is the angle at which the cannon is currently rotated
    cannon_angle = 0  
    
    angle_scale = 1
    #whether or not the cannon is firing
    weapon_firing = False
    #whether or not this object has gravity
    has_gravity = False     
    
    shots_fired = 0   
    
    def moveLeft(self, e):
        self.x -= 20
        self.xy = self.x - 100, self.y - 100, self.x + 100, self.y + 100
        self.stage.can.move(self.baseobj, -20, 0)        
        self.stage.can.update_idletasks()
        
    def moveRight(self, e):
        self.x += 20
        self.xy = self.x - 100, self.y - 100, self.x + 100, self.y + 100
        self.stage.can.move(self.baseobj, 20, 0)
        self.stage.can.update_idletasks()
    
    def calc(self):        
        
        deltaY = self.y - self.stage.mouse_y
        deltaX = self.x - self.stage.mouse_x                
        
        angle = math.atan2(deltaY, deltaX) / self.angle_scale

        self.x1 = 4 * math.degrees(math.cos(angle))
        self.y1 = 4 * math.degrees(math.sin(angle))
        self.cannon_head = self.x - self.x1, self.y - self.y1
        self.cannon_angle = angle
        
    
    def draw(self):
        self.stage.can.coords(self.cobj,
            self.cannon_head[0],
            self.cannon_head[1],
            self.x,
            self.y
        )        
    
    def __init__(self, stage={}):
        self.stage = stage
        self.x, self.y = stage.width / 2, stage.height
        self.xy = self.x - 100, self.y - 100, self.x + 100, self.y + 100
        
        self.baseobj = self.stage.can.create_arc(self.xy, start=0, extent=180, fill="red")
        deltaY = self.y - self.stage.mouse_y
        deltaX = self.x - self.stage.mouse_x
                
        angle = math.degrees(math.atan2(deltaY, deltaX)) / self.angle_scale
                
        x1 = -200 * math.cos(angle)
        y1 = -200 * math.sin(angle)
        
        self.cannon_head = self.x - x1, self.y - y1
        self.cannon_angle = angle
        cannon = self.stage.can.create_line(self.x - x1, self.y - y1, self.x, self.y, fill='red', width=20)
        self.cobj = cannon
        self.stage.world_objects["cannon"] = self 
        self.calc()