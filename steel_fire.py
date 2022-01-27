# STRUCTURAL ANALYSIS OF CROSS-SECTION SUBJECTED TO FIRE LOAD
# ACCORDING TO BS EN 1991-1-2
# AUTHOR: ELEFTHERIA TSALAMEGKA
# DATE: 25/01/2022


import math
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objs as go

# -----------------------------------------------------------------------------------------------
# INPUT PARAMETERS
# FIRE EVENT DURATION
t_min = 120  # Fire duration [min]
dt_sec = 5  # Time step [sec]

# MATERIAL USED
mat = 'steel'

if mat == 'steel':
    density = 7850  # Steel density [kg/m3]
else:
    density = 2700  # Aluminum density [kg/m3]

# CROSS-SECTION GEOMETRY
# Cross section type
# CS = 'SHS'
# CS = 'CHS'
CS = 'I'

# I-type cross-section dimensions
h = 400  # Web height [mm]
b = 180  # Flange width [mm]
tf = 13.5  # Flange thickness [mm]
tw = 8.6  # Web thickness [mm]

# CHS-type cross section dimensions
d_out = 100  # Outer diameter [mm]
t_chs = 13  # Wall thicknes [mm]

# SHS-type cross section dimensions
b_out = 100  # Outer diameter [mm]
t_shs = 13  # Wall thicknes [mm]

# PROTECTION COATING DATA
dp = 30  # Thickness [mm]
l_p = 0.15  # Thermal conductivity [W/m.K]
c_p = 1200  # Specific heat of the fire protection material [J/kg.K]
ro_p = 800  # Density of the protection material [kg/m^3]

# EMISSIVITY DATA
ef = 1  # Emissivity of the fire
em = 0.8  # Surface emissivity of the member
phi = 1  # Configuration factor
alpha_c = 25  # Coefficient of heat transfer by convection [W/m^2*K]
sigma = 5.67 * 10 ** -8  # Stephan Boltzmann constant [W/m^2*K^4]
th_ambient = 20  # Ambient temperature [C]

# -----------------------------------------------------------------------------------------------

# GEOMETRICAL CALCULATIONS
if CS == 'CHS':
    Am_V = 1 / t_chs  # Section factor for CHS cross section [m^-1]
    ksh = 1  # Shadow effect correction factor for CHS cross section
elif CS == 'SHS':
    Am_V = 1 / t_shs  # Section factor for SHS cross section [m^-1]
    ksh = 1  # Shadow effect correction factor for SHS cross section
elif CS == 'I':
    A = 2 * b * tf + (h - 2 * tf) * tw  # Cross-sectional area for I-type cross section [mm2]
    P = 2 * h +  b + 2 * (b - tw)  # Heated perimeter for I-type cross section [mm]
    Am_V = P / A  # Section factor for I-type cross section [m^-1]
    Pb = 2 * h + b  # Heated perimeter of "box" for I-type cross section
    Am_Vb = Pb / A  # Section factor of "box" for I-type cross section [m^-1]
    ksh = min(0.9 * Am_Vb / Am_V, 1)  # Shadow effect correction factor for I-type cross section


# -----------------------------------------------------------------------------------------------
# TEMPERATURE-TIME FIRE CURVES


def standard_curve(t):
    return 20 + 345 * np.log10(8 * t + 1)  # EN 1991-1-2, eqn.(3.4)


def external_curve(t):
    return 660 * (1 - 0.687 * np.e ** (-0.32 * t) - 0.313 * np.e ** (-3.8 * t)) + 20  # EN 1991-1-2 (2002), eqn.(3.5)


# -----------------------------------------------------------------------------------------------
# SPECIFIC HEAT

th_m = th_ambient  # Initial value for the surface temperature
dth_m = 0  # Initial value for the surface temperature increment


def specific_heat(t):
    if mat == 'steel':
        # J/kg C - Specific heat of steel - 3.4.1.2
        if th_m <= 600:
            c = 425 + 7.73 * 10 ** -1 * th_m - 1.69 * 10 ** -3 * t ** 2 + 2.22 * 10 ** -6 * t ** 3
        elif th_m <= 735:
            c = 666 + (13002 / (738 - t))
        elif th_m <= 900:
            c = 545 + (17820 / (t - 731))
        else:
            c = 650
    else:
        c = 0.41 * t + 903  # J/kg C - Specific heat of aluminium - 3.3.1.2
    return c


# -----------------------------------------------------------------------------------------------
# ANALYSIS OF UNPROTECTED SECTION

step_results_unprot = []

for t in np.arange(0, t_min * 60, dt_sec):
    # EN 1999-1-2 (4.10)
    factor = ksh * Am_V * 1000 * dt_sec / (specific_heat(th_m) * density)
    # EN 1991-1-2 (3.1)
    h_net_c = alpha_c * (standard_curve(t / 60) - th_m)
    h_net_r = phi * em * ef * sigma * ((standard_curve(t / 60) + 273) ** 4 - (th_m + 273) ** 4)

    th_m += dth_m
    dth_m = factor * (h_net_c + h_net_r)

    step_results_unprot.append([t, t / 60, standard_curve(t / 60), th_m, specific_heat(th_m), dth_m])

    results_unprot = pd.DataFrame(step_results_unprot,
                                  columns=['Time [sec]', 'Time [min]', 'θg [C]', 'θm [C]', 'c [J/kgC]', 'dθm [C]'])

print(results_unprot)

# -----------------------------------------------------------------------------------------------
# ANALYSIS OF PROTECTED SECTION

step_results_prot = []
dth = 0
for t in np.arange(0, t_min * 60, dt_sec):
    # EN 1999-1-2 (4.14, 4.13)
    phi_ = (c_p*ro_p)/(specific_heat(th_m)*density)*dp*Am_Vb
    dth_m = Am_V * 1000 * l_p / (dp * 10 ** -3 * specific_heat(th_m) * density) * (
            standard_curve(t / 60) - th_m) / (1 + phi_ / 3) * dt_sec - (math.e ** (phi_ / 10) - 1) * dth
    dt = specific_heat()
    dth_m = max(dth_m, 0)
    th_m += dth_m


    step_results_prot.append([t, t / 60, standard_curve(t / 60), th_m, specific_heat(th_m), dth_m])

    results_prot = pd.DataFrame(step_results_prot,
                                columns=['Time [sec]', 'Time [min]', 'θg [C]', 'θm [C]', 'c [J/kgC]', 'dθm [C]'])

print(results_prot)

# -----------------------------------------------------------------------------------------------
# PLOTTING

# Protected case
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=results_unprot['Time [min]'], y=results_unprot['θg [C]'], name="θg"))
fig1.add_trace(go.Scatter(x=results_unprot['Time [min]'], y=results_unprot['θm [C]'], name="θm"))
fig1.update_layout(
    title="Unprotected Cross-Section",
    xaxis_title="Time [min]",
    yaxis_title="Temperature [C]")
fig1.show()

# Unprotected Case
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=results_prot['Time [min]'], y=results_prot['θg [C]'], name="θg"))
fig2.add_trace(go.Scatter(x=results_prot['Time [min]'], y=results_prot['θm [C]'], name="θm"))
fig2.update_layout(
    title="Protected Cross-Section",
    xaxis_title="Time [min]",
    yaxis_title="Temperature [C]")
fig2.show()

# Collected
fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=results_prot['Time [min]'], y=results_prot['θg [C]'], name="Standard Fire Curve"))
fig3.add_trace(go.Scatter(x=results_prot['Time [min]'], y=results_prot['θm [C]'], name="Protected Member Temperature"))
fig3.add_trace(go.Scatter(x=results_unprot['Time [min]'], y=results_unprot['θm [C]'],
                          name="Unprotected Member Temperature"))
fig3.update_layout(
    title="Temperature-Time Curves",
    xaxis_title="Time [min]",
    yaxis_title="Temperature [C]")
fig3.show()

# Subplots
fig4 = make_subplots(rows=1, cols=2, shared_yaxes=True,
                     subplot_titles=("Unprotected Cross-Section", "Protected Cross-Section"))

# Subplot 1
# Temperature range subplot / Nominal WTs
fig4.append_trace(go.Scatter(
    x=results_unprot['Time [min]'],
    y=results_unprot['θg [C]'],
    mode='lines', line=dict(color="#636EFA"),
    name='Standard Temperature Fire Curve'), row=1, col=1)

# Temperature range subplot / Calculated WTs
fig4.append_trace(go.Scatter(
    x=results_unprot['Time [min]'],
    y=results_unprot['θm [C]'],
    mode='lines', line=dict(color="#636EFA", dash='dash'),
    name='Protected Member Temperature'), row=1, col=1)

fig4.append_trace(go.Scatter(
    x=results_prot['Time [min]'],
    y=results_prot['θg [C]'],
    mode='lines', line=dict(color="#EF553B"),
    name='Standard Temperature Fire Curve'), row=1, col=2)

# Temperature range subplot / Calculated WTs
fig4.append_trace(go.Scatter(
    x=results_prot['Time [min]'],
    y=results_prot['θm [C]'],
    mode='lines', line=dict(color="#EF553B", dash='dash'),
    name='Unprotected Member Temperature'), row=1, col=2)

fig4['layout']['yaxis']['title'] = 'Temperature [C]'
fig4['layout']['xaxis']['title'] = 'Time [min]'
fig4['layout']['xaxis2']['title'] = 'Time [min]'
fig4.update_layout(title_text="Temperature-Time Curves")

fig4.show()
# -----------------------------------------------------------------------------------------------
