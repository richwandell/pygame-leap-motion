import Leap, threading, sys, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
#from test2_modules.world_objects import Finger

class LeapListener(Leap.Listener):
    
    def on_init(self, cont):
        pass
        
    def on_connect(self, controller):        
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
        
    def on_disconnect(self, controller):
        pass
        
    def on_exit(self, controller):
        pass
        
    def on_frame(self, controller):
        frame = controller.frame()
        
#        print(dir(frame.gestures.im_class))
#        print(frame.gestures.im_self.id)
        
        if not frame.hands.empty:
            allhands = []
                        
            for hand in frame.hands:                
                fingers = hand.fingers
                if not fingers.empty:
                    positions = []
                    for f in fingers:
                        positions.append({
                            'id': f.id,
                            'tip_position': [f.tip_position[0], f.tip_position[1], f.tip_position[2]]
                        })
                    allhands.append({
                        'id': hand.id,
                        'fingers': positions,
                        'palm_position': [hand.palm_position[0], hand.palm_position[1], hand.palm_position[2]]
                    })

            self.hands = allhands

    
    
    