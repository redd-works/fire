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
b = 100 # mm
tf = 5 # mm
tw = 4 # mm

A = 2060 # mm2
Iy = 7135891.91 # mm4
Iz = 1415406.67 # mm4
J = 10366 # mm4
centr = 76

# Span
Lx = 780 # mm - Span of step
Ly = 2800 # mm - Main span

# Number of elements
n = 10

p_sdl = 0.35 # kPa
p_Q = 4 # kPa

P_G = 1 # kN
P_Q = 4 # kN


def loads(y_G, y_Q, psi,
        p_sdl=p_sdl,p_Q=p_Q, P_G=P_G, P_Q=P_Q,
        dp=40, density_p=115, l_p=400,
        Lx=Lx, A=A, rho=rho):

    w_prot = dp * l_p * density_p * g / 1e9
    w_self = A*10**-6 * rho * g / 1000 # kN/m
    w_sdl = p_sdl * Lx / 2 / 1000
    w_G = w_self + w_prot + w_sdl
    w_Q = p_Q * Lx / 2 / 1000

    w = (w_G*y_G + psi*w_Q*y_Q)
    P = (P_G*y_G + psi*P_Q*y_G) * 1000
    return w, P


def sec_I(h, b, tf, tw):
    # :params
    #     h: full depth
    #     b: width
    #     tf: flange thickness
    #     tw: web thickness
    # :return: Area, Iyy, Izz
    A = 3*b*tf + (h - 2*tf)*tw
    Iyy = ((h - 2*tf)**3*tw/12 + 2*b*tf**3/12 + 2*tf*b*((h - tf)/2)**2)
    Izz = 2*tf*b**3/12 + (h - 2*tf)*tw**3/12
    J = 1/3*(2*b*tf**3 + (h-2*tf)*tw**3)
    return A, Iyy, Izz, J

