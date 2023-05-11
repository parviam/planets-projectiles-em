print("importing numpy...", end='')
import numpy as np
print("done")

import("importing math...", end='')
import math
print("done")

#h_a - height where atmosphere ends (m)
def final_position(h_a):
    return numpy.array([0,0,h_a])

#m_s - mass of planet (kg)
#r_s - radius of planet (m)
def final_velocity(m_s, r_s, h_a):
    G = 6.67430 * 10**-11       #universal constant G
    return numpy.array([sqrt(G*m_s/(r_s + h)),0,0]) #based on a_c and newton with no atmosphere

def accel():    #determines acceleration of object, currently placeholder
    return -9.81

#v - current velocity (m/s)
#a - instantaneous acceleration (m/s^2)
#dt - very small change in time (s)

def new_v(v, a, dt):    #use kinematics to find new velocity after some dt
    return v + a*dt

def delta_x(a, v, dt):  #use kinematics to find displacement after some dt
    return .5 * a * dt**2 + v*dt

def at_ground(s, s_0):     #check if projectile is at ground level
    np.isclose(s, s_0)

s_0 = np.array([0,0,0]) #initial position

#test case: earth
    




