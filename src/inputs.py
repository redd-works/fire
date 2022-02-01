from scipy.constants import g
import numpy as np

# BS EN 1999-1-1: 3.2.5 Design values of material constants
fy = 240 # MPa
E = 70e3 # N/mm2
G = 27e3 # N/mm2
v = 0.3
alpha = 23e-6 # per C
rho = 2700 # kg/m3

# Section properties
h = 160  # mm
b = 100 # mm
tf = 5 # mm
tw = 4 # mm

A = 2060 # mm2
Iy = 7135891.91 # mm4
Iz = 1415406.67 # mm4
J = 10366 # mm4
centr = 76.46

# Span
Lx = 650 # mm - Span of step
Ly = 2770. # mm - Main span

# Number of elements
n = 10

# Loads
y_G = 1.35
y_Q = 1.5
y_G = 1.0
y_Q = 1.0

w_self = A*10**-6 * rho * g / 1000 # kPa
w_sdl = 0.5 # kPa
w_G = w_self + w_sdl
w_Q = 7 # kPa
pres = (w_G*y_G + w_Q*y_Q)*(10**-3) # N/mm2 - (kN/m2 = 10^-3N/mm2) - 10% safty factor
w = pres * Lx/2 # N/mm (= kN/m) - Uniformly distributed load

P_G = 1 # kN
P_Q = 4.5 # kN
P = P_G*y_G + P_Q*y_G

if __name__ == '__main__':
    print(w/b*1000)


