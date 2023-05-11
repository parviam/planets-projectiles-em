import numpy as np

def mag(vector):
    return np.linalg.norm(vector)

def new_v(m, g, k, v,dt):
    a = (m*g - k*mag(v)*v)/m
    return v + a*dt

def v_all(v_0,m,g,k,total_time,t,dt):
    v = np.array([v_0]) #velocity data w/ time in (m/s,m/s,m/s,s)
    while t < total_time:
        v = np.vstack((v, new_v(m,g,k,v[-1],dt)))
        t += dt
    return v

dt = 0.01 #time-step in s
total_time = 10 #time length of simulation in s
t = 0 #time variable
v_0 = np.array([0,0,0]) #velocity in m/s
m = 1  #mass of sattelite in kg


#test case: earth
g_earth = np.array([0,0,-9.81]) #g in m/s^2
k_earth = 0.24 #k coefficient in kg/m
print(v_all(v_0,m,g_earth,k_earth,total_time,t,dt))