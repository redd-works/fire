from inputs import *
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

def sec_c(h, b, tf, tw):
    # :params
    #     h: full depth
    #     b: width
    #     tf: flange thickness
    #     tw: web thickness
    # :return: Area, Iyy, Izz
    lb = 15
    lt = 10
    hw = 142.13
    tft = 3
    ret = 10
    A = b*tf + 2*lb*tf + hw*tw + b*tft + 2*lt*tf + 2*(ret*tft+7*tft) + 2*(42*tft+7*tft+12*tft) + 34*tft
    Iyy = ((h - 2*tf)**3*tw/12 + 2*b*tf**3/12 + 2*tf*b*((h - tf)/2)**2)
    Izz = 2*tf*b**3/12 + (h - 2*tf)*tw**3/12
    J = 1/3*(2*b*tf**3 + (h-2*tf)*tw**3)
    return A, Iyy, Izz, J


if __name__ == '__main__':
    It_e = 3.56e4 # mm4 - Torsional costant of UB152x89x16 of BlueBook
    A_e, Iyy_e, Izz_e, J_e = sec_I(h, b, tf, tw)
    print(A_e, Iyy_e, Izz_e)
