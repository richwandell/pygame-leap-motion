import math, time, hashlib
from collections import deque
import test2_modules.bullet
from pylab import *
import numpy as np

class WorldObject:
    """
    World objects will have an x and y coordinate. Objects that are set to have world recursion will appear at the opposite edge of the screen
    when they reach a screen edge. Objects that are set to have "has_gravity" will be given a positive 9.8 pixels in the y direction on each 
    logic tick. 
    
    Logic ticks happen at 16 millisecond intervals which should give the game a frame rate of 60fps if there is not an overwhelming amount of logic 
    to process.
    
    """
    #the current x position
    x = 0
    #the current y position
    y = 0
    #Boolean whether or not the world is recursive for this object, objects
    #leave on the right side and come out on the left
    world_recursion = True    
    #cobj is the canvas object reference that is used when moving the element 
    #or when deleteing the element from the canvas
    cobj = False            
    
    def checkObjectColision(self):
        """
        Check object colision uses the cojb to read the canvas coordinates of the current object 
        the coordinates are used in the find_overlapping canvas method to find any other objects that are 
        overlapping the current object.
        
        Any overlapping id's are hashed into there object_id and found in the world_objects dictionary by the id
        
        Finally, if the object has a method named 'collisionHandler' the method will be called with all of the overlapping 
        objects passed into the method.
        """
        coords = self.stage.can.coords(self.cobj)
        if len(coords) == 4:
            overlappers = self.stage.can.find_overlapping(coords[0], coords[1], coords[2], coords[3])
            
            ovr_objs = []
            for obj in overlappers:
                search_id = str(obj)
                if search_id in self.stage.world_objects:
                    ovr_objs.append(self.stage.world_objects[search_id])
            
            if "collisionHandler" in dir(self):
                self.collisionHandler(ovr_objs)
    
    def boundsReached(self, side):
        """
        When a world object reaches the outer bounds of the world, if the object has a property
        named 'world_recursion' the object will apear to go into one side of the world and come out the other.
        
        Finally, the bounds reached function will be called if there is a boundsReached method
        """
        if self.world_recursion:        
            map = {
                'left': (self.stage.width, self.y),
                'right': (0, self.y),
                'top': (self.x, self.stage.height),
                'bottom': (self.x, 0)
            }
            self.setPosition(map[side])
            
        if "boundsReachedHandler" in dir(self):
            self.boundsReachedHandler(side)
            
        return True
                    
    def checkScreenBounds(self):
        """
        Check to see if the object has reached the outer bounds of the 
        world, if so, we call the boundsReached method and pass in the side 
        """
        if self.x < 0:
            return self.boundsReached("left")
        elif self.x > self.stage.width:
            return self.boundsReached("right")
                        
        if self.y > self.stage.height-30:            
            return self.boundsReached("bottom")
        elif self.y < 0:
            return self.boundsReached("top")
        
        return False
    
    def draw(self):
        """
        Draw method must be implemented by any subclasses. Draw 
        will be called in the main draw loop to draw the object.
        """
        pass
    
    def calc(self):
        pass
        

class Animateable:
    
    def addVectors(self, (m1, a1), (m2, a2)):
        x1 = m1 * math.cos(a1)
        y1 = m1 * math.sin(a1)
        
        x2 = m2 * math.cos(a2)
        y2 = m2 * math.sin(a2)
        
        x = x1+x2
        y = y1+y2
        
        ma = math.sqrt(x**2 + y**2)
        
        angle = math.atan2(y, x)
        
        return (ma, angle)
    
    def setPosition(self, position):
        """
        Sets the current object center to a new position
        """
        self.x, self.y = position        
        coords = self.stage.can.coords(self.cobj)
        width = coords[2] - coords[0]
        height = coords[3] - coords[1]
        self.stage.can.coords(self.cobj, 
                              self.x - width / 2, 
                              self.y - height / 2,
                              self.x + width / 2,
                              self.y + height / 2)


    def move(self, x=0, y=0):
        """
        Moves an animatable object by the suplied x and y distance
        """
        self.x, self.y = self.x + x, self.y + y
                    
        self.stage.can.move(self.cobj, x, y)
        
        
class Crosshair(WorldObject):
    
    cobjs = []
    
    def draw(self):
        self.stage.can.coords(self.cobjs[0],
            self.stage.can.canvasx(self.stage.mouse_x) - 20,
            self.stage.can.canvasy(self.stage.mouse_y) - 20,
            self.stage.can.canvasx(self.stage.mouse_x) + 20,
            self.stage.can.canvasy(self.stage.mouse_y) + 20
        )
    
    def __init__(self, stage={}):
        self.stage = stage
        
        self.cobjs.append(self.stage.can.create_oval(
            self.stage.can.canvasx(self.stage.mouse_x) - 20,
            self.stage.can.canvasy(self.stage.mouse_y) - 20,
            self.stage.can.canvasx(self.stage.mouse_x) + 20,
            self.stage.can.canvasy(self.stage.mouse_y) + 20,
            fill="green"
        ))
            

class Ground(WorldObject):    
                                        
    def __init__(self, stage={}):
        self.stage = stage
        self.x, self.y = (0, self.stage.height)
        self.cobj = self.stage.can.create_line(self.x, self.y - 10, self.stage.width, self.y - 10, fill='red', width=20)      
        
class Finger(WorldObject):
    
    #a list of all fingers
    fingers = []
    
    #canvas objects for this finger
    cobjs = []
    
    def __init__(self, stage, finger, width=1, hand={}):
        self.stage = stage
        self.x = self.stage.width / 2 + (finger['tip_position'][0] * 5)
        self.y = self.stage.height - (finger['tip_position'][1] * 4)
        self.z = finger['tip_position'][2]
        
        Finger.fingers.append(self)
        xy = self.x - 10, self.y - 10, self.x + 10, self.y + 10
        self.cobjs.append(self.stage.can.create_oval(xy, fill="blue"))
        
        xy = self.stage.width / 2 + (hand['palm_position'][0]*5), (self.stage.height) - (hand['palm_position'][1]*4)
        
        self.cobjs.append(self.stage.can.create_line(self.x, self.y, xy[0], xy[1], fill='blue', width=2))
        
class Stats(WorldObject):
    
    stats = []
    
    count = 0            
    
    fr = 0
    
    start_or_finish = True
    
    def draw(self):
        self.count += 1

        if self.count % 5 == 0:
            if self.start_or_finish == True:
                self.start_time = time.time()
                self.start_or_finish = False
            else:
                self.end_time = time.time()
                self.start_or_finish = True
                
                self.fr = 5 / (self.end_time - self.start_time) 
        
        self.stage.can.dchars(self.stats[0], 0, 50)
        self.stage.can.insert(self.stats[0], "insert", "Framerate: %d" % self.fr)
        self.stage.can.dchars(self.stats[1], 0, 50)
        self.stage.can.insert(self.stats[1], "insert", "Bullets: %d" % len(test2_modules.bullet.Bullet.bullet_queue))
        self.stage.can.dchars(self.stats[2], 0, 50)
        self.stage.can.insert(self.stats[2], "insert", "World Objects: %d" % len(self.stage.world_objects))
        self.stage.can.dchars(self.stats[3], 0, 50)
        self.stage.can.insert(self.stats[3], "insert", "Canvas Objects: %d" % len(self.stage.can.find_all()))
        self.stage.can.dchars(self.stats[4], 0, 50)
        self.stage.can.insert(self.stats[4], "insert", "Cannon angle: %d" % int(self.stage.world_objects['cannon'].cannon_angle))        
        
    
    def __init__(self, stage):
        self.stage = stage
        self.t0 = time.time()
        
        self.count += 1

        if self.count % 5 == 0:
            if self.start_or_finish == True:
                self.start_time = time.time()
                self.start_or_finish = False
            else:
                self.end_time = time.time()
                self.start_or_finish = True
                
                self.fr = 5 / (self.end_time - self.start_time)                
        
        self.stats.append(self.stage.can.create_text((50, 20), text="Framerate: %d" % self.fr, fill="white"))
        self.stats.append(self.stage.can.create_text((50, 40), text="Bullets: %d" % len(test2_modules.bullet.Bullet.bullet_queue), fill="white")) 
        self.stats.append(self.stage.can.create_text((50, 60), text="World Objects: %d" % len(self.stage.world_objects), fill='white'))
        self.stats.append(self.stage.can.create_text((50, 80), text="Canvas Objects: %d" % len(self.stage.can.find_all()), fill='white'))
        self.stats.append(self.stage.can.create_text((50, 100), text="Cannon angle: %d" % self.stage.world_objects['cannon'].cannon_angle, fill='white'))
        
    
    
        
         
class Cube(WorldObject):
    
    points, lines = [], []
    
    connections = [
        [0, 1],
        [0, 2],
        [0, 4],
        [1, 3],
        [1, 5],
        [2, 3],
        [2, 6],
        [3, 7],
        [4, 5],
        [4, 6],            
        [5, 7],
        [6, 7]
    ]
    
    def __init__(self, stage):
        self.stage = stage        
        self.calc()
                            
        for point in self.pt:            
            xy = ((self.stage.width / 2) + (point[0]*1000 - 5)), (self.stage.height / 2) + (point[1]*1000 -5), (self.stage.width / 2) + (point[0]*1000 + 5), (self.stage.height / 2) + (point[1]*1000 +5)
            self.points.append(self.stage.can.create_oval(xy, fill='yellow'))
        
        
        for c in Cube.connections:
            self.lines.append(
                self.stage.can.create_line(
                    (self.stage.width / 2) + (self.pt[c[0]][0]*1000), 
                    (self.stage.height / 2) + (self.pt[c[0]][1] * 1000), 
                    (self.stage.width / 2) + (self.pt[c[1]][0]*1000), 
                    (self.stage.height / 2) + (self.pt[c[1]][1]*1000), 
                    fill='yellow', 
                    width=2 
                )
            )
            
    def draw(self):
        for x, point in enumerate(self.points):
            self.stage.can.coords(self.points[x], 
                (self.stage.width / 2) + (self.pt[x][0]*1000 - 5),
                (self.stage.height / 2) + (self.pt[x][1]*1000 -5),
                (self.stage.width / 2) + (self.pt[x][0]*1000 +5),
                (self.stage.height / 2) + (self.pt[x][1]*1000 +5) 
            )
            
        for x, c in enumerate(Cube.connections):
            self.stage.can.coords(self.lines[x],                
                (self.stage.width / 2) + (self.pt[c[0]][0]*1000), 
                (self.stage.height / 2) + (self.pt[c[0]][1] * 1000), 
                (self.stage.width / 2) + (self.pt[c[1]][0]*1000), 
                (self.stage.height / 2) + (self.pt[c[1]][1]*1000)
            )

        
    def calc(self):
        ## The cube vertices
        vs = reshape(mgrid[-1:2:2,-1:2:2,-1:2:2].T, (8,3))
        
        self.rotM = self.crazy_rotation(self.stage.world_objects['cannon'].cannon_angle*self.stage.world_objects['cannon'].angle_scale, 180)

        ## Calculate the 3D coordinates of the vertices of the rotated
        ## cube. Just multiply the vectors by the rotation matrix...
        self.vvs = dot(vs, self.rotM)

        ## Now calculate the image coordinates of the points.
        self.pt = self.project(-5, self.vvs)
        
        
            
    
    def quaternion_to_matrix(self, myx):
        """
        Produces a rotation matrix from the 3 last components of a
        quaternion.
        """
        # '''converts from a quaternion representation (last 3 values) to rotation matrix.'''
        xb,xc,xd = myx
    
        xnormsq = xb*xb+xc*xc+xd*xd
    
        if xnormsq < 1:
            ## If inside the unit sphere, these are the components
            ## themselves, and we just have to calculate a to normalize
            ## the quaternion.
            b,c,d = xb,xc,xd
            a = np.sqrt(1-xnormsq)
        else:
            ## Just to work gracefully if we have invalid inputs, we
            ## reflect the vectors outside the unit sphere to the other
            ## side, and use the inverse norm and negative values of a.
            b,c,d = -xb/xnormsq,-xc/xnormsq,-xd/xnormsq
            a = -np.sqrt(1-  1.0/xnormsq  )
            ## This should not be used, it defeats the whole concept that
            ## small (b,c,d) vector norms have small rotation angles. It's
            ## really just to let us work near the borders of the
            ## sphere. Any optimization algorithm should work with
            ## initalizations just inside the spere, and avoid wandering
            ## outside of it.
    
        assert a >= -1
        assert a <= 1
    
        ## Notice we return a transpose matrix, because we work with line-vectors
    
        return np.array([ [(a*a+b*b-c*c-d*d), (2*b*c-2*a*d),     (2*b*d+2*a*c)      ],
                             [(2*b*c+2*a*d),     (a*a-b*b+c*c-d*d), (2*c*d-2*a*b)      ],
                             [(2*b*d-2*a*c),     (2*c*d+2*a*b),     (a*a-b*b-c*c+d*d)] ]  ).T  \
                             / (a*a+b*b+c*c+d*d)
    
    
    
    def crazy_rotation(self, ind, Nind):
        """
        Calculate quaternion values using sinusoids over the frame index
        number, and get rotation matrix. Notice that the second parameter
        is the number of frames. That allows us to easily create an
        animation that can be played as a loop.
        """
        return self.quaternion_to_matrix(0.5*sin(pi*2*ind*Nind**-1.*array([1,2,3])))
    
    
    def project(self, D, vecs):
        """
        This function calculate the projected image coordinates form the 3D
        coordinates of the object vertices.
        """
        return self.vvs[:,:2]/(self.vvs[:,[2,2]]-D)













