#calculates initial velocity needed to reach orbital velocity at height of no atmosphere

print("importing numpy...", end='')
import numpy as np
print("done")

print("importing math...", end='')
import math
print("done")

def mag(vector):    #magnitude of a vector
    return np.linalg.norm(vector)

G = 6.67430 * 10**-11       #universal constant G

def g(m_s, r_s, h):     #calculates acceleration due to gravity at some height above a planet
    #m_s - mass of planet (kg)
    #r_s - radius of planet (m)
    #h - height of object above the surface (m)
    return np.array([0, 0, -G*m_s/(r_s+h)**2])   #from newton's law of universal gravitation

def rho(h):     #calculates volume density of air MARS ONLY - placeholder
    coefficient = 0.699*math.e**(-0.0009*h)/0.1921  #temp var for efficiency
    if h > 7000:
        return coefficient/(249.7-0.00222*h)
    return coefficient/(242.1-0.000998*h)

def c_d(rho_a,v_mag,r_b,mu,a_waves):    #calculates coefficient of drag using piecewise
    reynolds = rho_a*v_mag*2*r_b/mu     #reynolds number
    if reynolds < 0.2:
        return 24/reynolds
    coefficient = 21.12/reynolds + 6.3/math.sqrt(reynolds) + .25  #temp var for efficiency
    if reynolds < 2*10**3:
        return coefficient
    mach = v_mag/a_waves    #mach number, below only works for mach < 1
    return coefficient*(1-0.445*mach + 4.84*mach**2-9.73*mach**3+6.93*mach**4)/math.sqrt(1+1.2*mach*coefficient)

def drag_a(v, r_b, m_b, h, mu, a_waves):        #calculates drag acceleration in Newtons
    v_mag = mag(v)  #magnitude of v
    rho_a = rho(h)
    a = v_mag**2*math.pi*r_b**2*rho_a*c_d(rho_a,v_mag,r_b,mu, a_waves)/(2*m_b)
    return a        

def accel(m_s, r_s, h, v, r_b, m_b, mu, a_waves):    #determines acceleration of object
    return g(m_s, r_s, h) + drag_a(v, r_b, m_b, h, mu, a_waves)/m_s     #newton's second law

def final_position(h_a):
    #h_a - height where atmosphere ends (m)
    return np.array([0,0,h_a])


def final_velocity(m_s, r_s, h_a):      #find final orbital (goal) velcocity of object
    #m_s - mass of planet (kg)
    #r_s - radius of planet (m)
    return np.array([math.sqrt(G*m_s/(r_s + h_a)),0.,0.]) #based on a_c and newton with no atmosphere

def new_v(v, a, dt):    #use backwards kinematics to find new velocity after some dt
    #v - current velocity (m/s)
    #a - instantaneous acceleration (m/s^2)
    #dt - very small change in time (s)
    return v - a*dt

def delta_x(a, v, dt):  #use backwards kinematics to find displacement after some dt
    return .5 * a * dt**2 - v*dt

def at_ground(s, s_0):     #check if projectile is at ground level
    return abs(s[2] - s_0[2]) < 1

def get_initial_v(s_0, m_s, r_s, h_a, r_b, m_b, mu, a_waves, dt):
    s = final_position(h_a) #current position variable (m)
    v = final_velocity(m_s,r_s,h_a) #current velocity variable (m/s)
    t_count = 0 #printing counter
    while not at_ground(s, s_0):
        a = accel(m_s,r_s,s[2],v, r_b, m_b, mu, a_waves)    #current acceleration variable (m/s^2)
        s = s + delta_x(a, v, dt)   #changes position with displacement calculation
        v = new_v(v, a, dt)     #changes velocity with displacement calculation

        t_count += dt       #printing feedback system
        if t_count % 10 < dt:
            print("calculated until", t_count, "sec; z-position is equal to:", s[2])
            
    return v
        
dt = 0.0001 #change in time constant (s)
s_0 = np.array([0.,0.,0.]) #initial position (m)

#test case: earth ==> INCOMPLETE
r_earth = 6.3781 *10**6 #radius of earth in m
m_earth = 5.9722 * 10**24 #mass of earth in kg
h_a_earth = 100000 #end of atmosphere in meters
#print("v:", get_initial_v(s_0, m_earth, r_earth, h_a_earth, dt))


