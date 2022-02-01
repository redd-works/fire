from inputs import *
import argparse
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

