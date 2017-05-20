import time
from test2_modules.bullet import Bullet
from test2_modules.world_objects import Finger
            
    

class AnimationController:
    """
    Animation controller is a simple mixin that holds only the draw loop for our stage.
    
    Any drawing activities are handled in the same main loop
    """
        
    
    def handleFingers(self):                        
        
        for finger in Finger.fingers:
            for obj in finger.cobjs:
                self.can.delete(obj)
        
        Finger.fingers = []
        
        for hand in self.hands:
            for finger in hand['fingers']:
                Finger(
                    self,
                    finger=finger,
                    width=1,   
                    hand=hand
                )
            
                
    def drawLoop(self):   
        """
        Draw loop is used to do all the drawing. 
        All drawing has to be on this same loop and not in any other threads or else the game
        will freeze!
        """                               
        self.handleFingers()        
        
        
        for _id, wo in self.world_objects.items():
            wo.calc()            
            wo.draw()            
            
        #re schedule the draw loop         
        self.can.after(16, func=self.drawLoop)
        
        
        
        
        
        
        
        