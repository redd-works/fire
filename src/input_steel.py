""" 
INPUT_STEEL.PY DOCUMENTATION

-----------------

Input_steel.py sets up the method required in order to read the steel_section.xlsx file, 
along with 2 other methods to calculate factored loads (loads) and section properties (sec_I).
Different materials can be added to steel_section.xlsx.

"""

from scipy.constants import g
import pandas as pd
import yaml

#dict_steel_sect={}



df = pd.read_excel("steel_sections.xlsx") # read excel file and store as dataframe
     
dict_steel_sect = df.to_dict('index') # Transform data frame to dictionary

def chooseSection():  # the following method allows the user to choose a certain 
                        # section for the program to run calculations on.
          
    """ 
    This method will allow the user to select the sections he wishes to test, 
    it does so by converting the excel file into a dictionary and then asking for user input. 
    It will return the index of the chosen section in the dictionary.

    :return name: val
    :return type: int

    """
    print(yaml.dump(dict_steel_sect, sort_keys=False, default_flow_style=False))  
    val = int(input("Pick Section: \n"))
    print(yaml.dump(dict_steel_sect[val], sort_keys=False, default_flow_style=False))
    return val

val = chooseSection() # for testing purposes


# BS EN 1999-1-1: 3.2.5 Design values of material constants
def getType(val):
    material = dict_steel_sect[val].get('Type')
    return material
    
    
def getFy(val):
    fy = dict_steel_sect[val].get('Fy (MPa)')  # MPa
    return fy

def getE(val):
    E = dict_steel_sect[val].get('E (N/mm2)') # N/mm2
    return E
    
def getG(val):   
    G = dict_steel_sect[val].get('G (N/mm2)') # N/mm2
    return G

def getV(val):   
    v = dict_steel_sect[val].get('v')
    return v

def getAlpha(val):    
    alpha = dict_steel_sect[val].get('alpha (per C)') # per C
    return alpha
    
def getRho(val):
    rho = dict_steel_sect[val].get('rho (Kg/m3)') # kg/m3
    return rho
    

# Section properties
def getH(val):    
    h = dict_steel_sect[val].get('h (mm)')  # mm
    return h

def getB(val):
    b = dict_steel_sect[val].get('b (mm)') # mm
    return b

def getTf(val):
    tf = dict_steel_sect[val].get('tf (mm)') # mm
    return tf

def getTw(val):
    tw = dict_steel_sect[val].get('tw (mm)') # mm
    return tw


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


def loads(rho, y_G, y_Q, psi,  # calculate loads placed on section
       p_sdl=p_sdl,p_Q=p_Q, P_G=P_G, P_Q=P_Q,
        dp=40, density_p=115, l_p=400,
        Lx=Lx, A=A):
     
     
     
    """ 

    Calculate factored loads.

    :return name: w: distributed load,
                  P: Point load


    """

    w_prot = dp * l_p * density_p * g / 1e9
    w_self = A*10**-6 * rho * g / 1000 # kN/m
    w_sdl = p_sdl * Lx / 2 / 1000
    w_G = w_self + w_prot + w_sdl
    w_Q = p_Q * Lx / 2 / 1000

    w = (w_G*y_G + psi*w_Q*y_Q)
    P = (P_G*y_G + psi*P_Q*y_G) * 1000
    return w, P




def sec_I(h, b, tf, tw):  # calculate section properties
    # :params
    #     h: full depth
    #     b: width
    #     tf: flange thickness
    #     tw: web thickness
    # :return: Area, Iyy, Izz
     
     
    """ 

    Calculate section properties
    :parameters: h: depth of section,
                 b: width of section,
                 tw: web thickness,
                 tf: flange thickness

    :return name: A: area (mm2),
                  Iyy : 2nd moment of inertia about y axis,
                  Izz : 2nd moment of inertia about z axis,
                  J: radius of gyration
    """
    A = 3*b*tf + (h - 2*tf)*tw
    Iyy = ((h - 2*tf)**3*tw/12 + 2*b*tf**3/12 + 2*tf*b*((h - tf)/2)**2)
    Izz = 2*tf*b**3/12 + (h - 2*tf)*tw**3/12
    J = 1/3*(2*b*tf**3 + (h-2*tf)*tw**3)
    return A, Iyy, Izz, J

#print(sec_I(h,b,tf,tw))
