#calculates initial velocity needed to reach orbital velocity at height of no atmosphere

print("importing numpy...", end='')
import numpy as np
print("done")

print("importing math...", end='')
import math
import random
print("done")

print("importing matplotlib...", end = '')
import matplotlib.pyplot as plt
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

def temp(h):        #calculates temperature  MARS ONLY 
    h_km = h/1000 #height in km
    if h_km > 300:
        raise ValueError("height is higher than 3000!")
    if h_km > 115:
        zet = (h_km-120)*(3.38951 + 120)/(3389.51 + h_km)
        return 200 - 72.225 * math.exp(-0.0195 * zet)
    if h_km > 105:
        return 203.25 - 0.65 * h_km
    if h_km > 95:
        return 282 - 1.40 * h_km
    if h_km > 84:
        return 149
    if h_km > 75:
        return -61 + 2.5 * h_km
    if h_km > 66:
        return 314 - 2.5 * h_km
    if h_km > 55:
        return 106.1 + 0.65 * h_km
    if h_km > 48:
        return 271.10 - 2.35 * h_km
    if h_km > 39:
        return 158.30
    if h_km > -8:
        return 228.5 - 1.8 * h_km
    else:
        raise ValueError("height is less than -8!! and is actually", h)
def pressure(h):        #calculates pressure at height ONLY MARS 
    h_km = h/1000 #height in km
    if h_km > 300:
        raise ValueError("height is higher than 3000!")
    if h_km > 200:
        return math.exp(-4.83452E-11*h_km**5 + 6.96178E-08*h_km**4 - 4.03197E-05*h_km**3 + 0.0117655*h_km**2 - 1.76494*h_km + 93.67154)
    if h_km > 120:
        return math.exp(-4.18520E-10*h_km**5 + 3.45846E-07*h_km**4 - 1.13352E-04*h_km**3 + 0.0188613*h_km**2 - 1.71718*h_km + 61.10381)
    if h_km > 105:
        return 0.00169282 * (135/(135 - 0.65*(h_km-105)))**(-19.435/0.65)
    if h_km > 95:
        return 0.00666032 * (149/(149 - 1.40*(h_km-95)))**(-19.435/1.40)
    if h_km > 84:
        return 0.0279653*math.exp(-19.435*(h_km-84)/149.00)
    if h_km > 75:
        return 0.0998430 * (126.50/(126.50 +2.50*(h_km-75)))**(19.435/2.50)
    if h_km > 66:
        return 0.356464 * (149.0/(149.0 - 2.50*(h_km-66)))**(-19.435/2.50)
    if h_km > 55:
        return 1.55091 * (141.85/(141.85 + 0.65*(h_km-55)))**(19.435/0.65)
    if h_km > 48:
        return 3.84305 * (158.30/(158.35 - 2.35*(h_km-48)))**(19.435/-2.35)
    if h_km > 39:
        return 11.6025 * math.exp(-19.435*(h_km-39)/158.30)
    if h_km > -8:
        return 610.5 * (228.50/(228.50-1.80*h_km))**(-19.435/1.8)
    raise ValueError("height is less than -8!")
def mach(v_mag, t):     #calculates velocity of sound ONLY MARS
    heat_r = 0.000001409*(t**2) - 0.001192*t + 1.5175       #specific heat ratio
    gas_const = 191.181     #specific gas constant of mars
    v_sound = math.sqrt(heat_r*gas_const*t) #sound speed
    return v_mag/v_sound
def knudsen(t, mach, reynolds):
    heat_r = 0.000001409*(t**2) - 0.001192*t + 1.5175       #specific heat ratio
    return math.sqrt(math.pi*heat_r/2)*mach/reynolds

def rho(h, t):     #calculates volume density of air MARS ONLY
    h_km = h/1000
    if h_km > 300:
        raise ValueError("height > 300!!")
    if h_km > 200:
        return math.exp(2.65472E-11*h_km**5 - 2.45558E-08*h_km**4 + 6.31410E-06*h_km**3 + 4.73359E-04*h_km**2 - 0.443712*h_km + 23.79408)
    if h_km > 120:
        return math.exp(-2.55314E-10*h_km**5 + 2.31927E-07*h_km**4 - 8.33206E-05*h_km**3 + 0.0151947*h_km**2 - 1.52799*h_km + 48.69659)
    p = pressure(h)
    return p/(191.181*t)
def viscosity(t):      #calculates viscosity of air based on 100% CO2 MARS ONLY
    mu_0 = 1.370e-5 #viscosity constant 
    s_c = 222 #sutherland's constant
    t_0 = 273 #temperature cosntant, kelvin ratio
    return mu_0*(t/t_0)**(3/2)*((t_0 + s_c)/(t+s_c))    #sutherland's law
        
def c_d(rho_a,v_mag,r_b,t, h):    #calculates coefficient of drag using piecewise
    mu = viscosity(t)       #viscosity of air at height
    reynolds = rho_a*v_mag*2*r_b/mu     #reynolds number
    mach_no = mach(v_mag, t)
    knudsen_no = knudsen(t,mach_no,reynolds)
    if reynolds < 2e5 and reynolds < 10e6 and knudsen_no < 0.01:
        return 24/reynolds*(1 + 0.15 * reynolds**0.687) + 0.42/(1+(42500/reynolds**1.16))
    if reynolds > 10e3 and mach_no < 1.5:
        return 1.65 + 0.65*math.tanh(4*mach_no-3.4)
    if reynolds > 10e3 and reynolds < 10e6 and mach_no > 1.5:
        return 2.18 - 0.13*math.tanh(0.9*mach_no-2.7)/100
    return 0

def drag_a(v, r_b, m_b, h):        #calculates drag acceleration in Newtons
    t = temp(h)     #temperature of air at height
    v_mag = mag(v)  #magnitude of v
    rho_a = rho(h, t)  #density of air
    a = v_mag**2*math.pi*r_b**2*rho_a*c_d(rho_a,v_mag,r_b,t, h)/(2*m_b)
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
    return abs(s[2] - s_0[2]) < 1000

def get_initial_v(s_0, m_s, r_s, h_a, r_b, m_b, dt):
    s = final_position(h_a) #current position variable (m)
    v = final_velocity(m_s,r_s,h_a) #current velocity variable (m/s)
    t_count = 0 #printing counter
    v_store = np.array([])
    while not at_ground(s, s_0):
        a = accel(m_s,r_s,s[2],v, r_b, m_b)    #current acceleration variable (m/s^2)
        s = s + delta_x(a, v, dt)   #changes position with displacement calculation
        v = new_v(v, a, dt)     #changes velocity with displacement calculation
        #v_store = np.append(v_store, v[2])
        t_count += dt       #printing feedback system
        if t_count % 10 < dt or (t_count % 1 < dt and s[2] < 70000):
            print(a, v, "m/s vertical at", s[2], "m above ground at", t_count, "s")
    print(t_count)
    return v

#Testing Suite

dt = 0.001 #change in time constant (s)
s_0 = np.array([0.,0.,0.]) #initial position (m)

#mars calculations
r_mars = 3389.5 * 10**3 #radius of mars (m)
m_mars = 6.39 * 10**23 #mass of mars (kg)
h_a_mars = 230000 #height of atmosphere on mars (m)
r_b = 10 #radius of ball (m)
m_b = 10000 #mass of ball (kg)

print(get_initial_v(s_0,m_mars,r_mars,h_a_mars,r_b,m_b,dt))



