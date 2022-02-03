import inputs as inp

y_G = 1.35
y_Q = 1.5

p_sdl = 0.5 # kPa
p_Q = 4 # kPa

w_self = inp.A*10**-6 * inp.rho * inp.g / 1000 # kN/m
w_sdl = p_sdl*inp.Lx / 2 / 1000
w_G = w_self + w_sdl

w_Q = p_Q * inp.Lx / 2 / 1000
w = (w_G*y_G + 0.1*w_Q*y_Q) # kN/m - N/mm - UDL

P_G = 1 # kN
P_Q = 4 # kN
P = P_G*y_G + 0.1*P_Q*y_G

if __name__ == '__main__':
    print(w_G, w_Q, w)


