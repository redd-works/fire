import openseespy.opensees as ops
import openseespy.postprocessing.ops_vis as opsv
import matplotlib.pyplot as plt
from scipy.constants import g
import secprop


# TODO: Properties under fire 65% of the original one - See "Fire.ipynb" notebook
# BS EN 1999-1-1: 3.2.5 Design values of material constants
E = 70e3 # N/mm2
G = 27e3 # N/mm2
v = 0.3
alpha = 23e-6 # per C
rho = 2700 # kg/m3

# Section properties
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
pres = 1.1*(w_G*y_G + 0.1*w_Q*y_Q)*(10**-3) # N/mm2 - (kN/m2 = 10^-3N/mm2) - 10% safty factor
w = pres * Lx/2 # N/mm (= kN/m) - Uniformly distributed load

# OpenSees model
ops.wipe()
ops.model('basic', '-ndm', 3, '-ndf', 6)

mid = int(n/2)+1
for i in range(n+1):
    ops.node(i+1, 0., i*Ly/n, 0.)

ops.fix(1, 1, 1, 1, 0, 1, 1)
ops.fix(n+1, 1, 1, 1, 0, 1, 1)

gTTagy = 1

coordTransf = 'Linear'
ops.geomTransf(coordTransf, gTTagy, 1., 0., 0.)

for i in range(1, n+1):
    ops.element('elasticBeamColumn', i, i, i+1, A, E, G, J, Iz, Iy, gTTagy)

Ew = {}

Pz = w*Ly/n # N

ops.timeSeries('Constant', 1)
ops.pattern('Plain', 1, 1)
for i in range(1, n+1):
    ops.load(i, 0., 0., Pz, 0., 0., 0.)

ops.constraints('Transformation')
ops.numberer('RCM')
ops.system('BandGeneral')
#ops.test('NormDispIncr', 1.0e-6, 6, 2)
ops.algorithm('Linear')
ops.integrator('LoadControl', 1)
ops.analysis('Static')
ops.analyze(1)

### Post-process
disp = ops.nodeDisp(mid, 3)
print(disp)
disp_e = 5/384*(w*Ly**4)/(E*Iy)
print(disp_e)

minY, maxY = opsv.section_force_diagram_3d('Vy', Ew, 1.)
plt.title(f'Transverse force Vy [N], max = {maxY:.2e}, min {minY:.2e}')

minY, maxY = opsv.section_force_diagram_3d('Mz', Ew, 1.)
plt.title(f'Bending moments Mz [Nmm], max = {maxY:.2e}, min {minY:.2e}')

plt.show()
