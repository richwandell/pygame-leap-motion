
from libc.math cimport sin, cos

cdef mvbullet(int x, int y, int m, int sh,  long double t,  long double t0, int v0x, int v0y, double ay, double theta):
    """
    x coordinate, y coordinate, mass, stage height, initial time
    """
    cdef int spos    
    cdef long double dt
    cdef long double vx
    cdef long double vy    
    
    spos = 0
    
    if y > sh - (30 + m):                        
        t0 = t
        v0y = v0y - 5
        if v0y < 1:
            v0y = 0
            spos = 1

        if v0y == 0:
            v0x -= 1
        if v0x < 0: v0x = 0
        
    dt = t - t0

    vx = v0x
    vy = v0y + (ay * dt)
                    
    #change in x is velocity times cos(theta)
    dx = vx * cos(theta)
    #change in y is velocity times sin(theta)
    dy = vy * sin(theta)
    
    return dt, v0x, v0y, vx, vy, dx, dy, spos

def bullet(int x, int y, int m, int sh,  long double t,  long double t0, int v0x, int v0y, double ay, double theta):
    return mvbullet(x, y, m, sh, t, t0, v0x, v0y, ay, theta)

def say_hello():
    print "Hello World!"