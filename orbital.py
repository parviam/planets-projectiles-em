#calculates initial velocity needed to reach orbital velocity at height of no atmosphere

print("importing numpy...", end='')
import numpy as np
print("done")

print("importing math...", end='')
import math
print("done")



#Newton's Second Law Suite

def mag(vector):    #magnitude of a vector
    return np.linalg.norm(vector)

G = 6.67430 * 10**-11       #universal constant G

def g(m_s, r_s, h):     #calculates acceleration due to gravity at some height above a planet
    #m_s - mass of planet (kg)
    #r_s - radius of planet (m)
    #h - height of object above the surface (m)
    return np.array([0, 0, -G*m_s/(r_s+h)**2])   #from newton's law of universal gravitation

def temp(h):        #calculates temperature in kelvin ==>BROKEN
    return 210.372 #avg temp placeholder
    if h > 7000:
        return -23.4-0.00222*h + 273.15
    return -31 - 0.000998 * h + 273.15

def v_sound(h, t):     #calculates velocity of sound
    coefficient = 1.289*0.1889/44.01
    return math.sqrt(coefficient * t)

def rho(h, t):     #calculates volume density of air MARS ONLY
    return 0.699*math.e**(-0.0009*h)/(0.1921*t)  #temp var for efficiency

def viscosity(h, t):      #calculates viscosity of air MARS ONLY
    coefficient = 0.01480 *(0.555*527.67+240)       #temp var for efficiency
    coefficient /= 0.555*(5/9*t) + 240
    coefficient *= (5/9*t/527.67)**(3/2)
    return coefficient
        
def c_d(rho_a,v_mag,r_b,h,t):    #calculates coefficient of drag using piecewise
    mu = viscosity(h,t)       #viscosity of air at height
    reynolds = rho_a*v_mag*2*r_b/mu     #reynolds number
    if reynolds < 0.2:
        return 24/reynolds
    coefficient = 21.12/reynolds + 6.3/math.sqrt(reynolds) + .25  #temp var for efficiency
    if reynolds < 2*10**3:
        return coefficient

    a_waves = v_sound(h, t)    #velocity of sound at height
    mach = v_mag/a_waves    #mach number, below only works for mach < 1
    return coefficient*(1-0.445*mach + 4.84*mach**2-9.73*mach**3+6.93*mach**4)/math.sqrt(1+1.2*mach*coefficient)

def drag_a(v, r_b, m_b, h):        #calculates drag acceleration in Newtons
    t = temp(h)     #temperature of air at height
    v_mag = mag(v)  #magnitude of v
    rho_a = rho(h, t)  #density of air
    a = v_mag**2*math.pi*r_b**2*rho_a*c_d(rho_a,v_mag,r_b,h,t)/(2*m_b)
    return -a*v/v_mag        

def accel(m_s, r_s, h, v, r_b, m_b):    #determines acceleration of object
    return g(m_s, r_s, h) + drag_a(v, r_b, m_b, h)     #newton's second law




#Kinematics Suite


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

def get_initial_v(s_0, m_s, r_s, h_a, r_b, m_b, dt):
    s = final_position(h_a) #current position variable (m)
    v = final_velocity(m_s,r_s,h_a) #current velocity variable (m/s)
    t_count = 0 #printing counter
    v_store = np.array([])
    while not at_ground(s, s_0):
        a = accel(m_s,r_s,s[2],v, r_b, m_b)    #current acceleration variable (m/s^2)
        s = s + delta_x(a, v, dt)   #changes position with displacement calculation
        v = new_v(v, a, dt)     #changes velocity with displacement calculation
        t_count += dt       #printing feedback system
        v_store = np.append(v_store, v[2])
        if v[2] > 10**25:
            break
    return v

#Testing Suite

dt = 0.001 #change in time constant (s)
s_0 = np.array([0.,0.,0.]) #initial position (m)

#mars calculations
r_mars = 3389.5 * 10**3 #radius of mars (m)
m_mars = 6.39 * 10**23 #mass of mars (kg)
h_a_mars = 230000 #height of atmosphere on mars (m)
r_b = 1 #radius of ball (m)
m_b = 1 #mass of ball (kg)

print(get_initial_v(s_0,m_mars,r_mars,h_a_mars,r_b,m_b,dt))



