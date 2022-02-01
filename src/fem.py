import numpy as np
import openseespy.opensees as ops
import openseespy.postprocessing.ops_vis as opsv
import matplotlib.pyplot as plt
import inputs as inp

def model(w=inp.w, P=inp.P,
          n=inp.n, L=inp.Ly,
          fy=inp.fy, E=inp.E, G=inp.G, 
          A=inp.A, Iy=inp.Iy, Iz=inp.Iz, J=inp.J, centr=inp.centr, h=inp.h,
          plot=False):  

    # OpenSees model
    ops.wipe()
    ops.model('basic', '-ndm', 3, '-ndf', 6)

    mid = int(n/2)+1
    for i in range(n+1):
        ops.node(i+1, 0., i*L/n, 0.)

    ops.fix(1, 1, 1, 1, 0, 1, 1)
    ops.fix(n+1, 1, 1, 1, 0, 1, 1)

    gTTagy = 1

    coordTransf = 'Linear'
    ops.geomTransf(coordTransf, gTTagy, 1., 0., 0.)

    for i in range(1, n+1):
        ops.element('elasticBeamColumn', i, i, i+1, A, E, G, J, Iz, Iy, gTTagy)

    Ew = {}

    Pz = w*L/n # N
    P *= 1000 # N
    if P*4 > Pz*L:
        Pz = 0
    else:
        P = 0

    ops.timeSeries('Constant', 1)
    ops.pattern('Plain', 1, 1)
    for i in range(1, n+1):
        ops.load(i, 0., 0., -Pz, 0., 0., 0.)
        if i%(n/5) == 1 and i != n:
            ops.load(i, 0., 0., -P, 0., 0., 0.)

    ops.constraints('Transformation')
    ops.numberer('RCM')
    ops.system('BandGeneral')
    ops.algorithm('Linear')
    ops.integrator('LoadControl', 1)
    ops.analysis('Static')
    ops.analyze(1)

    ### Post-process
    disp = ops.nodeDisp(mid, 3)
    disp_e = -5/384*((w+P*4/L)*L**4)/(E*Iy)
    print("Disp from fea: {:.3f} mm, hand calcs {:.3f} mm".format(disp, disp_e))
    print("L/d = {:.3f}".format(L/disp))
    Myy = ops.eleForce(mid, 4)
    stress = Myy*(h - centr)/Iy
    print("Stress util: {:.3f}".format(stress/fy))
    print("First frequency: {:.3f}".format(17.8/(np.abs(disp)**0.5)))

    if plot:
        minY, maxY = opsv.section_force_diagram_3d('Vy', Ew, 1.)
        plt.title(f'Transverse force Vy [N], max = {maxY:.2e}, min {minY:.2e}')

        minY, maxY = opsv.section_force_diagram_3d('Mz', Ew, 1.)
        plt.title(f'Bending moments Mz [Nmm], max = {maxY:.2e}, min {minY:.2e}')

        plt.show()

if __name__ == "__main__":
    model(w, P)
