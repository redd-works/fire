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
n = 20

# Loads
y_G = 1.35
y_Q = 1.5

p_sdl = 0.5 # kPa
p_Q = 4 # kPa

w_self = A*10**-6 * rho * g / 1000 # kN/m
w_sdl = p_sdl*Lx / 2 / 1000
w_G = w_self + w_sdl

w_Q = p_Q * Lx / 2 / 1000
w = (w_G*y_G + w_Q*y_Q) # kN/m - N/mm - UDL

P_G = 0.2 # kN
P_Q = 4 # kN
P = P_G*y_G + P_Q*y_G

if __name__ == '__main__':
    print(w_G, w_Q, w)


