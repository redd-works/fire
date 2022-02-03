import argparse
import inputs as inp
import fire
import fem

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

    fy, E = inp.fy, inp.E
    if args.fire:
        fy, E = fire.temperature(plot=args.plot)

    fem.model(fy=fy, E=E, plot=args.plot)  







    

