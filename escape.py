print("importing numpy...", end='')
import numpy as np
print("done")

print("importing math...", end='')
import math
print("done")

#h_a - height where atmosphere ends (m)
def final_position(h_a):
    return np.array([0,0,h_a])

#m_s - mass of planet (kg)
#r_s - radius of planet (m)
def final_velocity(m_s, r_s, h_a):
    G = 6.67430 * 10**-11       #universal constant G
    #return np.array([math.sqrt(G*m_s/(r_s + h_a)),0.,0.]) #based on a_c and newton with no atmosphere
    return np.array([math.sqrt(2*G*m_s/r_s),0,0])       #formula from online that seems to work?

def accel(v):    #determines acceleration of object, currently placeholder
    return np.array([0,0,-9.81])

#v - current velocity (m/s)
#a - instantaneous acceleration (m/s^2)
#dt - very small change in time (s)

def new_v(v, a, dt):    #use backwards kinematics to find new velocity after some dt
    return v - a*dt

def delta_x(a, v, dt):  #use backwards kinematics to find displacement after some dt
    return .5 * a * dt**2 - v*dt

def at_ground(s, s_0):     #check if projectile is at ground level
    return abs(s[2] - s_0[2]) < 1

def get_initial_v(s_0, m_s, r_s, h_a, dt):
    s = final_position(h_a) #current position variable (m)
    v = final_velocity(m_s,r_s,h_a) #current velocity variable (m/s)
    t_count = 0 #printing counter
    while not at_ground(s, s_0):
        a = accel(v)    #current acceleration variable (m/s^2)
        s = s + delta_x(a, v, dt)   #changes position with displacement calculation
        v = new_v(v, a, dt)     #changes velocity with displacement calculation

        t_count += dt       #printing feedback system
        if t_count % 10 < dt:
            print("calculated until", t_count, "sec")
            
    return v
        
dt = 0.0001 #change in time constant (s)
s_0 = np.array([0.,0.,0.]) #initial position (m)

#test case: earth
r_earth = 6.3781 *10**6 #radius of earth in m
m_earth = 5.9722 * 10**24 #mass of earth in kg
h_a_earth = 10800 #end of atmosphere in meters
print("v:", get_initial_v(s_0, m_earth, r_earth, h_a_earth, dt))


