import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Internal

def temp_in(t):
    return 20 + 345*np.log10(8*t + 1) # 3.4
def temp_ex(t):
    return 660*(1 - 0.687*np.e**(-0.32*t) - 0.313*np.e**(-3.8*t)) + 20 # 3.5

# Inputs

# Time
tm = 60 # min - Assumed, better make it 120 min
degree_sign = u'\N{DEGREE SIGN}'
tms = np.arange(0., tm, 1)

# Geometry
# Chords
section_type = 'CHS'
dc = 30e-3 # m
tc = 3e-3 # m
#Webs
dw = 10e-3 # m


print('Max External temerature of {:.0f} {}C'.format(temp_ex(tm), degree_sign))
print('-----------------')
print('Max Internal temerature of {:.0f} {}C'.format(temp_in(tm), degree_sign))

plt.plot(tms, temp_in(tms), 'r--',tms, temp_ex(tms), 'b')
plt.legend(['Internat', 'External'])
plt.title('Temperature action')
plt.xlabel('t (min)')
plt.ylabel('T {}C'.format(degree_sign))
plt.show()

def temp_unprot(section_type, tc, t_dur, temp_type, dt=5, th_m=20, Phi = 1.0, eps_m = 0.8, eps_f = 1.0,
                alp_c=25, ro_al=2700, sig=5.67e-8):
    """ Unprotected internal aluminium members BS EN 1999-1-2 (4.10)
    
    Parameters
    ----------
    section_type : str
        Only CHS supported
    tc : float
        Thickness of tube
    t_dur : float (min)
        The time duration
    temp_type : function
        External or internal fire
    dt : float (s)
        The time step (default is 5)
    th_m : flobal (Cels)
        The initial material temperature
    Phi: float
        The configuration factor (default is 1.0 - corresponding to fully developed fire)
    eps_m: float
        The surface emissivity of the member (default is 1.0 from NOTE1)
    eps_f: float
        The emissivity of the fire
    alp_c: float (W/m2.K)
        The coefficient of heat transfer (default is 25 for convection (3.4))
    ro_al: float (kg/m3)
        The density of aluminium (default is 2700)
    sig: float (W/m2.K4)
        The Stephan Boltzmann constant (default is 5.67e-8)
        
    Returns
    --------
    list
        of time
    list
        of temperautres
    
    """
    Am_V = 1. / tc # Table 3
    Am_Vb = 1. / tc
    k_sh = min(0.9 * Am_Vb/Am_V, 1.0)
    if section_type == 'CHS' or section_type == 'RHS' or section_type == 'SHS':
        k_sh = 1.0

    header = ['t (sec)', 't (min)', 'th_g (deg)', 'th_m (deg)', 'c_al (J/kg.K)', 'dth_m (Cel)']
    data = []
    ts = 0  # sec - time
    ts_s = np.arange(0, t_dur*60, dt)

    # Initial temperature
    th_ms = []
    for ts in ts_s:
        # BS EN 1991-1-2
        tm = ts/60 # min = time
        c_al = 0.41*th_m + 903 # J/kg C - Specifi heat of aluminium - 3.3.1.2 
        th_g = temp_type(tm)
        h_net_c = alp_c * (th_g - th_m) # (3.2)
        h_net_r = Phi * eps_m * eps_f * sig * ((th_g + 273)**4 - (th_m + 273)**4) # (3.3)
        h_net = h_net_c + h_net_r # (3.1) - W/m2

        dth_m = k_sh * 1. / (c_al * ro_al) * Am_V * h_net * dt # 4.10
        th_ms.append(th_m)
        data.append([ts, tm, th_g, th_m, c_al, dth_m])

        th_m += dth_m
        ts += dt
    
    df = pd.DataFrame(data, columns=header)
    return ts_s, np.array(th_ms)

ts_s, th_ms = temp_unprot('CHS', tc, tm, temp_in)
plt.plot(tms, temp_in(tms), 'r', ts_s/60, th_ms, '--r')
ts_s, th_ms = temp_unprot('CHS', tc, tm, temp_ex)
plt.plot(tms, temp_ex(tms), 'b', ts_s/60, th_ms, '--b')

plt.legend(['Internat load', 'Internal temp', 'External load', 'External temp'])
plt.title('Temperature action')
plt.xlabel('t (min)')
plt.ylabel('T {}C'.format(degree_sign))
plt.show()


def temp_prot(section_type, tc, t_dur, temp_type, c_p = 1200, lam_p = 0.1, dp = 40e-3, ro_p = 900, dt=30, th_m=20, ro_al=2700):
    """ Unprotected internal aluminium members BS EN 1999-1-2 (4.10)

    Parameters
    ----------
    section_type : str
        Only CHS supported
    tc : float
        Thickness of tube
    t_dur : float (min)
        The time duration
    temp_type : function
        External or internal fire
    c_p : float (J/kg.K)
        The specific heat of the fire protection material (default = 1200)
    lam_p : float (W/m.K)
        The thermal conductivity of the fire protection material (default = 0.1)
    dp : float (m)
        The thickness of the fire protection material
    ro_p : float (kg/m3)
        The density of the fire protection material
    dt : float (s)
        The time step (default is 5)
    th_m : flobal (Cels)
        The initial material temperature
    ro_al: float (kg/m3)
        The density of aluminium (default is 2700)

    Returns
        List of time and temperature
    --------
    """
    Ap_V = 1. / tc # Table 3

    header = ['t (sec)', 't (min)', 'th_g (deg)', 'th_m (deg)', 'c_al (J/kg.K)', 'phi', 'dth_m (Cel)']
    data = []
    ts = 0  # sec - time
    ts_s = np.arange(0, t_dur*60, dt)

    # Initial temperature
    th_ms = []
    dth = 0
    for ts in ts_s:
        # BS EN 1991-1-2
        tm = ts/60 # min = time
        c_al = 0.41*th_m + 903 # J/kg C - Specifi heat of aluminium - 3.3.1.2
        th_g = temp_type(tm)

        # BS EN 1999-1-2
        phi = c_p*ro_p*dp/(c_al*ro_al)*Ap_V # (4.14)

        dth_m = Ap_V*lam_p/(dp*c_al*ro_al)*(th_g - th_m)/(1+phi/3)*dt - (math.e**(phi/10) -1)*dth # (4.13)
        dth_m = max(dth_m, 0)
        th_ms.append(th_m)
        data.append([ts, tm, th_g, th_m, c_al, phi, dth_m])

        dth = temp_type(tm + dt/60) - th_g
        th_m += dth_m
        ts += dt

    df = pd.DataFrame(data, columns=header)
    return ts_s, np.array(th_ms)

ts_s, th_ms = temp_prot('CHS', tc, tm, temp_in)
plt.plot(tms, temp_in(tms), 'r', ts_s/60, th_ms, '--r')
print(th_ms[-1])
ts_s, th_ms = temp_prot('CHS', tc, tm, temp_ex)
print(th_ms[-1])
plt.plot(tms, temp_ex(tms), 'b', ts_s/60, th_ms, '--b')

plt.legend(['Internat load', 'Internal temp', 'External load', 'External temp'])
plt.title('Temperature action')
plt.xlabel('t (min)')
plt.ylabel('T {}C'.format(degree_sign))
plt.show()



"""
Solution
Use intumescent paint with the following thermal propoerties:
Thermal conductivity lam_p <= 0.1 W/(m.K)
Specifit heat: c_p >= 1200 J/kg.K
Desity: ro_p >= 900 kg/m3
Uniform thickness: d_p >= 40mm
This was we loose less than 35% of strength (see Table 1a) and less than 14# of Elastic modulues (see Table 2)
"""
