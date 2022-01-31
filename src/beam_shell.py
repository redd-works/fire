import akantu as aka
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = [10, 10]

material_input = """
material elastic [
    name = aluminium
    rho = 2700   # desnity
    E   = 70e10 # young's modulus
    v   = 0.3    # poisson's ratio
]"""

material_file = 'material.dat'
open(material_file, 'w').write(material_input)
aka.parseInput(material_file)

h = 1.
mesh_file = f"""
Point(1)  = {{ 0   ,	-158.5	, 0, {h}}};
Point(2)  = {{ 18.5,	-53.5	, 0, {h}}};
Point(3)  = {{ 11.5,	-11.5	, 0, {h}}};
Point(4)  = {{ 44.5,	-158.5	, 0, {h}}};
Point(5)  = {{ 0   ,     -158.5	, 0, {h}}};
Point(6)  = {{-44.5,	-158.5	, 0, {h}}};
Point(7)  = {{-50  ,     -158.5	, 0, {h}}};
Point(8)  = {{-18.5,	-63.5	, 0, {h}}};
Point(9)  = {{-48.5,	-63.5	, 0, {h}}};
Point(10) = {{18.5 ,     -63.5	, 0, {h}}};
Point(11) = {{48.5 ,     -63.5	, 0, {h}}};
Point(12) = {{-48.5,	-53.5	, 0, {h}}};
Point(13) = {{-48.5,	-63.5	, 0, {h}}};
Point(14) = {{48.5 ,     -53.5	, 0, {h}}};
Point(15) = {{48.5 ,     -63.5	, 0, {h}}};
Point(16) = {{-18.5,	-53.5	, 0, {h}}};
Point(17) = {{18.5 ,     -53.5	, 0, {h}}};
Point(18) = {{18.5 ,     -11.5	, 0, {h}}};
Point(19) = {{18.5 ,     -1.5	, 0, {h}}};
Point(20) = {{-18.5,	-11.5	, 0, {h}}};
Point(21) = {{-18.5,	-1.5	, 0, {h}}};
Point(22) = {{-11.5,	-1.5	, 0, {h}}};
Point(23) = {{-18.5,	-1.5	, 0, {h}}};
Point(24) = {{11.5 ,     -1.5	, 0, {h}}};
Point(25) = {{18.5 ,     -1.5	, 0, {h}}};
Point(26) = {{-11.5,	-11.5	, 0, {h}}};
Point(27) = {{0,	-11.5	, 0, {h}}};
Point(28) = {{11.5,	-11.5	, 0, {h}}};
Point(29) = {{0,	-11.5	, 0, {h}}};
Point(30) = {{44.5,	-158.5	, 0, {h}}};
Point(31) = {{-44.5,	-158.5	, 0, {h}}};
"""

