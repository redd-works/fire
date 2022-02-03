import argparse
import inputs as inp
import fire
import sees
import openseespy.opensees as ops
import openseespy.postprocessing.ops_vis as opsv
import numpy as np

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='FEA of beam under fire')

    parser.add_argument(
        '-p', '--plot', type=bool,
        help=('Choose to plot or not the solution.'
              ' True/False'), default=False)
    parser.add_argument(
        '-f', '--fire', type=bool,
        help=('Include fire in the analysis?'
              ' True/False'), default=False)
    parser.add_argument(
        '-l', '--load', type=str,
        help=('Type of design'
              ' Can be uls/sls'), default='uls')
    args = parser.parse_args()

    if args.load == 'sls':
        w, P = inp.loads(1., 1., 1., P_Q=0)
    else:
        w, P = inp.loads(1.35, 1.5, 1.)

    fy, E = inp.fy, inp.E
    if args.fire:
        w, P = inp.loads(1.35, 1.5, 0.1)
        fy, E = fire.temperature(plot=args.plot)

    sees.model(w=w, P=P, fy=fy, E=E)  

    ### Post-process
    mid = int(inp.n/2)+1
    disp = ops.nodeDisp(mid, 3)
    disp_e = -5/384*((w+P*4/inp.L)*inp.L**4)/(E*inp.Iy)
    print("Disp from fea: {:.3f} mm, hand calcs {:.3f} mm".format(disp, disp_e))
    print("L/d = {:.3f}".format(-inp.L/disp))
    Myy = ops.eleForce(mid, 4)
    stress = Myy*(inp.h - inp.centr)/inp.Iy
    print("Stress util: {:.3f}".format(-stress/inp.fy))
    print("First frequency: {:.3f}".format(17.8/(np.abs(disp)**0.5)))

    if args.plot:
        minY, maxY = opsv.section_force_diagram_3d('Vy', Ew, 1.)
        plt.title(f'Transverse force Vy [N], max = {maxY:.2e}, min {minY:.2e}')

        minY, maxY = opsv.section_force_diagram_3d('Mz', Ew, 1.)
        plt.title(f'Bending moments Mz [Nmm], max = {maxY:.2e}, min {minY:.2e}')

        plt.show()





    

