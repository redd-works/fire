## Import geometry from Rhino "P2112 Design model 03.3dm"
### Cross-section verification
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


h = 160  # mm
b = 86 # mm
tf = 5 # mm
tw = 4 # mm

It_e = 3.56e4 # mm4 - Torsional costant of UB152x89x16 of BlueBook

if __name__ == '__main__':
    A_e, Iyy_e, Izz_e, J_e = sec_I(h, b, tf, tw)
    print(A_e, Iyy_e, Izz_e)
