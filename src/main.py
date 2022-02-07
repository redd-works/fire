"""
MAIN.PY DOCUMENTATION

------------------------

In main.py, fire.py will be executed and calculations will be made depending on the loading condition.


"""


import input_steel as inp   
import argparse
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

    value = inp.chooseSection() # values = index of section chosen in dictionary
    
    A, Iyy, Izz, J = inp.sec_I(inp.getH(value),inp.getB(value), 
                               inp.getTf(value),inp.getTw(value))


    if args.load == 'sls':  # calculate loads based on load case
        w, P = inp.loads(1., 1., 1., P_Q=0, rho = inp.getRho(value))
    elif args.load == 'dyn':
        w, P = inp.loads(1., 1., 0.1, rho = inp.getRho(value))
    else:
        w, P = inp.loads(1.35, 1.5, 1., rho = inp.getRho(value))



    fy, E = inp.getFy(value), inp.getE(value)  # get Fy and E of chosen section
    if args.fire:                               # calculate fire loads
        w, P = inp.loads(1.35, 1.5, 0.1, rho = inp.getRho(value))
        fy, E = fire.temperature(fy=inp.getFy(value), E = inp.getE(value),t_min=120, mat=inp.getType(value),
                                    b=inp.getB(value), h=inp.getH(value), tf=inp.getTf(value), tw=inp.getTw(value),plot=args.plot)

    model.run(w=w, P=P, fy=fy, E=E, plot=args.plot)  

    mid = int(inp.n/2)+1
    if args.load == 'sls':
        disp = ops.nodeDisp(mid, 3)
        disp_e = -5/384*((w+P*4/inp.Ly)*inp.Ly**4)/(E*Iyy)
        print("Disp from fea: {:.3f} mm, hand calcs {:.3f} mm".format(disp, disp_e))
        print("L/d = {:.3f}".format(-inp.Ly/disp))
    elif args.load == 'dyn':
        disp = ops.nodeDisp(mid, 3)
        print("First frequency: {:.3f}".format(17.8/(np.abs(disp)**0.5)))
    else:
        Myy = ops.eleForce(mid, 4)
        stress = Myy*(inp.getH(value) - inp.centr)/Iyy
        print("Stress util: {:.3f}".format(-stress/inp.getFy(value)))
