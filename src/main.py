import argparse
import inputs as inp
import fire
import fem
import loads_uls as uls
import loads_sls as sls
import loads_fire as fir

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
        w, P = sls.w, sls.P
    else:
        w, P = uls.w, uls.P

    fy, E = inp.fy, inp.E
    if args.fire:
        w, P = fir.w, fir.P
        fy, E = fire.temperature(plot=args.plot)

    fem.model(w=w, P=P, fy=fy, E=E, plot=args.plot)  







    

