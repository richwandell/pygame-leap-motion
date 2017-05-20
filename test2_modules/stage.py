import time, sys, os, Leap
from Tkinter import Canvas
from test2_modules.animation_controller import AnimationController
from test2_modules.world_objects import Ground, Stats, Cube, Crosshair
from test2_modules.bullet import Bullet
from test2_modules.cannon import Cannon
from test2_modules.leap_classes import LeapListener


class Stage(AnimationController, LeapListener):
    #objects that will have physics applied to them
    world_objects = {}
    #place holder for the mouse x and y coordinates
    mouse_x, mouse_y = 0, 0 
    
    hands = []
    
    def mouseMoved(self, e):
        """
        Event handler for moving the mouse on the canvas
        This will set the mouse_x and mouse_y to the current mouse
        coordinates
        """        
        self.mouse_x, self.mouse_y = int(e.x), int(e.y)
        
    
    def startFiringWeapon(self, e):
        """
        Creates a new bullet at the tip of the cannon head once 
        every 30 milliseconds until the Stage.weapon_firing bool
        is false. At which time the thread will break out of its loop and die
        """
        def keepFiring():
            if Cannon.weapon_firing == True:  
                sound = self.bullet_snd.play()                
                Bullet(
                    position = self.world_objects["cannon"].cannon_head,
                    stage = self,                    
                    velocity = (-60, self.world_objects["cannon"].cannon_angle),
                )
                self.can.after(50, func=keepFiring)
        Cannon.weapon_firing = True
        keepFiring()

    def stopFiringWeapon(self, e):
        """
        Stops your gun from firing when you release the mouse button
        """        
        Cannon.weapon_firing = False
            
            
    def __init__(self, root, snack): 
        self.snack = snack
        
        self.click_loop = snack.Sound()
        self.click_loop.load('test2_sounds/185768__jobro__click-loop.wav')        
                    
        self.bullet_snd = snack.Sound()
        self.bullet_snd.load('test2_sounds/gun.wav')        

        #set resolution to screen width
        self.width = root.winfo_screenwidth()
        self.height = root.winfo_screenheight()
        root.wm_attributes('-fullscreen', 1)
        #create a canvas to draw on
        self.can = Canvas(root, cursor='none', width=self.width, height=self.height, background="black")
        self.can.pack()
        
        def playMusic():            
            self.click_loop.play()
            info = self.click_loop.length(units="SECONDS")
            self.can.after(int(info) * 1000, playMusic)
        #playMusic()
        
        #bind canvas events
        self.can.bind("<Motion>", self.mouseMoved)
        
        
        #create a cannon
        c = Cannon(self)
        self.world_objects["cannon"] = c
        
        root.bind("a", c.moveLeft)
        root.bind("d", c.moveRight)
        
        def exit(e):
            pid = os.getpid()
            os.kill(pid, 9)
        
        root.bind("<Escape>", exit)
        self.can.bind("<ButtonPress-1>", self.startFiringWeapon)
        self.can.bind("<ButtonRelease-1>", self.stopFiringWeapon)
        
        #create the ground
        self.world_objects["ground"] = Ground(self)
        self.world_objects["stats"] = Stats(self)
        self.world_objects["cube"] = Cube(self)
        self.world_objects["crosshair"] = Crosshair(self)
        
        LeapListener.__init__(self)
        self.leap_controller = Leap.Controller()
        self.leap_controller.add_listener(self)
        
        
        #create my draw loop
        self.drawLoop()
        
        
        
        
        
        
        
        
        
        
        
        
        
        