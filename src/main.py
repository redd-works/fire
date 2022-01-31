import openseespy.opensees as ops
import openseespy.postprocessing.ops_vis as opsv
import matplotlib.pyplot as plt
import argparse
import numpy as np
from inputs import *
import fire

def interpolation(x, x1, x2, y1, y2):
    return y1 + (y2-y1)/(x2-x1)*x


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='FEA of beam under fire')

    parser.add_argument(
        '-p', '--plot', type=bool,
        help=('Choose to plot or not the solution.'
              ' True/False'), default=False)

    parser.add_argument(
        '-f', '--fire', type=bool,
        help=('Whether to include fire in the analysis'
              ' True/False'), default=False)
    args = parser.parse_args()

    if args.fire:
        temp = fire.temp
        temp1 = int(temp - temp%50)
        temp2 = temp1 + 50
        temp_diff = temp - temp1
        if temp2 > 400:
            f_red = 0
        else:
            f1 = fire.strength_red[temp1]
            f2 = fire.strength_red[temp2]
            f_red = interpolation(temp_diff, temp1, temp2, f1, f2)
        fy *= f_red
        E1 = fire.stiff_red[temp1]
        if temp2 > 400:
            temp2 = 550
        E2 = fire.stiff_red[temp2]
        E_red = interpolation(temp_diff, temp1, temp2, E1, E2)
        E *= E_red

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
    Pv *= 1000 # N
    if Pv*4 > Pz*Ly:
        Pz = 0
    else:
        Pv = 0

    ops.timeSeries('Constant', 1)
    ops.pattern('Plain', 1, 1)
    for i in range(1, n+1):
        ops.load(i, 0., 0., -Pz, 0., 0., 0.)
        if i%(n/5) == 1 and i != n:
            ops.load(i, 0., 0., -Pv, 0., 0., 0.)

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
    disp_e = -5/384*((w+Pv*4/Ly)*Ly**4)/(E*Iy)
    print("Disp from fea: {:.3f} mm, hand calcs {:.3f} mm".format(disp, disp_e))
    print("L/d = {:.3f}".format(Ly/disp))
    Myy = ops.eleForce(mid, 4)
    stress = Myy*(h - centr)/Iy
    print("Stress util: {:.3f}".format(stress/fy))
    print("First frequency: {:.3f}".format(17.8/(np.abs(disp)**0.5)))

    if args.plot:
        minY, maxY = opsv.section_force_diagram_3d('Vy', Ew, 1.)
        plt.title(f'Transverse force Vy [N], max = {maxY:.2e}, min {minY:.2e}')

        minY, maxY = opsv.section_force_diagram_3d('Mz', Ew, 1.)
        plt.title(f'Bending moments Mz [Nmm], max = {maxY:.2e}, min {minY:.2e}')

        plt.show()
