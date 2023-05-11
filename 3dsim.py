import numpy as np
import matplotlib.pyplot as plt

def g_planet(m_p, r):   #returns acceleration due to gravity at a radius and mass of planet
    G = 6.67430 * 10**-11       #universal constant G
    return np.array([0,0,G*m_p/(r**2)])     #formula from universal gravitation

def mag(vector):    #magnitude of a vector
    return np.linalg.norm(vector)

def new_a(m,g,k,v): #use newtons 2nd law, for k and g on a planet, to find acceleration
    return (m*g - k*mag(v)*v)/m

def new_v(a, v,dt):       #use kinematics to find new v
    return v + a*dt     

def delta_s(a,v,dt):    #use kinematics to find displacement
    return .5 * a * (dt**2) + v*dt

def s_all(s_0,v_0,m,m_p,r_s,k, total_time,t_0,dt): #create table of all position data given initial conditions and time contraints
    t = t_0 #time variable
    v = v_0 #velocity variable
    s = np.array([s_0]) #will store all position data
    while t < total_time:
        g = g_planet(m_p, r_s + s[-1,2]) #calculating acceleration due to gravity
        a = new_a(m,g,k,v)  #find new acceleration
        s = np.vstack((s,s[-1]+delta_s(a,v,dt)))    #add row with new position data to table
        v = new_v(a, v, dt) #find new v given dt for next operation
        t += dt #incrrement time
    return s

dt = 0.01 #time-step in s
total_time = 10 #time length of simulation in s
t_0 = 0 #initial time in s

v_0 = np.array([0,0,0]) #initial velocity in m/s
s_0 = np.array([0,0,0]) #inital position in m
m = 1  #mass of sattelite in kg


#test case: earth
k_earth = 0.001 #k coefficient in kg/m
r_earth = 6.3781 *10**6 #radius of earth in m
m_earth = 5.9722 * 10**24 #mass of earth in kg
s_earth = s_all(s_0,v_0,m,m_earth,r_earth,k_earth,total_time,t_0,dt)
print(s_earth)

#test 2d plotting
time_plot = np.arange(t_0,total_time+dt*2,dt) #time as x-axis series, dt*2 b/c exclusive
plt.plot(time_plot,s_earth[:,-1])   #plot z-axis vs. time

#test 3d plotting ==> still janky
fig = plt.figure()
ax = plt.axes(projection="3d")
ax.scatter3D(s_earth[:,0], s_earth[:,1], s_earth[:,2])

plt.show()
