from scipy.constants import g

# BS EN 1999-1-1: 3.2.5 Design values of material constants
fy = 240 # MPa
E = 70e3 # N/mm2
G = 27e3 # N/mm2
v = 0.3
alpha = 23e-6 # per C
rho = 2700 # kg/m3

# Section properties
h = 160  # mm
b = 86 # mm
tf = 5 # mm
tw = 4 # mm

A = 1970 # mm2
Iy = 7368686.58 # mm4
Iz = 1069586.78 # mm4
J = 10366.66 # mm4

# Span
Lx = 610 # mm - Span of step
Ly = 2770. # mm - Main span

# Number of elements
n = 20

# Loads
y_G = 1.0
y_Q = 1.0
w_self = A*10**-6 * rho * g / 1000 # kN/m3
w_sdl = 0.1 # kN/m
w_G = w_self + w_sdl
w_Q = 4 # kPa
pres = (w_G*y_G + 0.1*w_Q*y_Q)*(10**-3) # N/mm2 - (kN/m2 = 10^-3N/mm2) - 10% safty factor
w = pres * Lx/2 # N/mm (= kN/m) - Uniformly distributed load


