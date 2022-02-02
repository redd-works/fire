import argparse
import inputs as inp
import fire
import fem

if __name__ == '__main__':
    """
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
    """

    f = True 
    p = True
    fy, E = inp.fy, inp.E
    if f:
        fy, E = fire.temperature(plot=p)

    fem.model(fy=fy, E=E, plot=p)  







    

