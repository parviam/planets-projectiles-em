import numpy as np

def mag(vector):
    return np.linalg.norm(vector)

def dx(m, g, k, v, dt):
    a = (m*g - k*mag(v)*v)/m
    return (1/2 * a * (dt)**2 + v*dt)
    
#test case: earth

v_0 = np.array([0,0,0]) #velocity in m/s
g = np.array([0,0,-9.81]) #g in m/s^2
m = 1  #mass of sattelite
k = 0.24 #k coefficient in kg/m
dt = 0.01 #time-step



