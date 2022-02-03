import argparse
import inputs as inp
import fire
import model
import numpy as np
import openseespy.opensees as ops

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
    elif args.load == 'dyn':
        w, P = inp.loads(1., 1., 0.1)
    else:
        w, P = inp.loads(1.35, 1.5, 1.)

    fy, E = inp.fy, inp.E
    if args.fire:
        w, P = inp.loads(1.35, 1.5, 0.1)
        fy, E = fire.temperature(t_min=120, plot=args.plot)

    model.run(w=w, P=P, fy=fy, E=E, plot=args.plot)  

    mid = int(inp.n/2)+1
    if args.load == 'sls':
        disp = ops.nodeDisp(mid, 3)
        disp_e = -5/384*((w+P*4/inp.Ly)*inp.Ly**4)/(E*inp.Iy)
        print("Disp from fea: {:.3f} mm, hand calcs {:.3f} mm".format(disp, disp_e))
        print("L/d = {:.3f}".format(-inp.Ly/disp))
    elif args.load == 'dyn':
        disp = ops.nodeDisp(mid, 3)
        print("First frequency: {:.3f}".format(17.8/(np.abs(disp)**0.5)))
    else:
        Myy = ops.eleForce(mid, 4)
        stress = Myy*(inp.h - inp.centr)/inp.Iy
        print("Stress util: {:.3f}".format(-stress/inp.fy))



