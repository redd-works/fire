import openseespy.opensees as ops
import openseespy.postprocessing.ops_vis as opsv
import matplotlib.pyplot as plt
import sec_prop
import argparse
from inputs import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='FEA of beam under fire')


    parser.add_argument(
        '-p', '--plot', type=bool,
        help=('Choose to plot or not the solution.'
              ' True/False'), default=False)

    args = parser.parse_args()

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
    Myy = ops.eleForce(mid, 4)
    sig_ed = Myy*(h/2)/Iy
    sig_rd = 200
    disp_e = 5/384*(w*Ly**4)/(E*Iy)
    print("Disp from fea: {:.3f} mm, hand calcs {:.3f} mm".format(disp, disp_e))

    if args.plot:
        minY, maxY = opsv.section_force_diagram_3d('Vy', Ew, 1.)
        plt.title(f'Transverse force Vy [N], max = {maxY:.2e}, min {minY:.2e}')

        minY, maxY = opsv.section_force_diagram_3d('Mz', Ew, 1.)
        plt.title(f'Bending moments Mz [Nmm], max = {maxY:.2e}, min {minY:.2e}')

        plt.show()
