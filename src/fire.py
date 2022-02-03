import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import plotly.express as px
import inputs as inp

# For 6061 T6
strength_red = { 20 : 1.00,
                100 : 0.95,
                150 : 0.91,
                200 : 0.79,
                250 : 0.55,
                300 : 0.31,
                350 : 0.10,
                400 : 0.00}

# For 6061 T6
stiff_red = { 20 : 1.00,
              50 : 0.99,
             100 : 0.97,
             150 : 0.93,
             200 : 0.86,
             250 : 0.78,
             300 : 0.68,
             350 : 0.54,
             400 : 0.40,
             550 : 0.00}

def interpolation(x, x1, x2, y1, y2):
    return y1 + (y2-y1)/(x2-x1)*x


def internal_curve(t):
    return 20 + 345 * np.log10(8 * t + 1)  # EN 1991-1-2, eqn.(3.4)


def external_curve(t):
    return 660 * (1 - 0.687 * np.e ** (-0.32 * t) - 0.313 * np.e ** (-3.8 * t)) + 20  # EN 1991-1-2 (2002), eqn.(3.5)


def specific_heat(mat, t):
    if mat == 'steel':
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


def temperature(fy=inp.fy, E = inp.E,
                t_min=60, dt_sec=5, mat='aluminium', CS='I',
                b=inp.b, h=inp.h, tf=inp.tf, tw=inp.tw, Am_Vb=0, ksh=1,
                prot_type='fibcem_coating', dp=40, l_p=0.036, c_p=0.65, density_p=115,
                ef=1, em=0.8, phi=1, alpha_c=25, sigma=5.67e-8, th_ambient=20,
                fire_curve=internal_curve, plot=False):

    if mat == 'steel':
        density = 7850  # Steel density [kg/m3]
    else:
        density = 2700  # Aluminum density [kg/m3]

    # GEOMETRICAL CALCULATIONS
    if CS == 'CHS':
        Am_V = 1 / t_chs  # Section factor for CHS cross section [m^-1]
        ksh = 1  # Shadow effect correction factor for CHS cross section
    elif CS == 'SHS':
        Am_V = 1 / t_shs  # Section factor for SHS cross section [m^-1]
        ksh = 1  # Shadow effect correction factor for SHS cross section
    elif CS == 'I':
        A = 2 * b * tf + (h - 2 * tf) * tw  # Cross-sectional area for I-type cross section [mm2]
        P = 2 * h + b + 2 * (b - tw)  # Heated perimeter for I-type cross section [mm]
        Am_V = P / A  # Section factor for I-type cross section [m^-1]
        Pb = 2 * h +  b  # Heated perimeter of "box" for I-type cross section
        Am_Vb = Pb / A  # Section factor of "box" for I-type cross section [m^-1]
        ksh = min(0.9 * Am_Vb / Am_V, 1)  # Shadow effect correction factor for I-type cross section

    # ----------------------------------------------------------------------------------------------------------------------
    # SPECIFIC HEAT

    th_m = th_ambient  # Initial value for the surface temperature
    dth_m = 0  # Initial value for the surface temperature increment


    # ----------------------------------------------------------------------------------------------------------------------
    # ANALYSIS OF UNPROTECTED SECTION

    step_results_unprot = []

    for t in np.arange(0, t_min * 60, dt_sec):
        factor = ksh * Am_V * 1000 * dt_sec / (specific_heat(mat, th_m) * density)
        h_net_c = alpha_c * (fire_curve(t / 60) - th_m)
        h_net_r = phi * ef * em * sigma * ((fire_curve(t / 60) + 273) ** 4 - (th_m + 273) ** 4)

        th_m += dth_m
        dth_m = factor * (h_net_c + h_net_r)

        step_results_unprot.append([t, t / 60, fire_curve(t / 60), th_m, specific_heat(mat, th_m), dth_m])

        results_unprot = pd.DataFrame(step_results_unprot,
                                      columns=['Time [sec]', 'Time [min]', 'θg [C]', 'θm [C]', 'c [J/kgC]', 'dθm [C]'])

    # ----------------------------------------------------------------------------------------------------------------------
    # ANALYSIS OF PROTECTED SECTION

    th_m = th_ambient  # Initial value for the surface temperature
    dth_m = 0  # Initial value for the surface temperature increment

    step_results_prot = []

    if prot_type == 'paint_coating':
        for t in np.arange(0, t_min * 60, dt_sec):
            th_m += dth_m

            dth_m = Am_V * 1000 * l_p / (dp * 10 ** -3 * specific_heat(mat, th_m) * density) * (
                    fire_curve(t / 60) - th_m) * dt_sec

            step_results_prot.append([t, t / 60, fire_curve(t / 60), th_m, specific_heat(mat, th_m), dth_m])

            results_prot = pd.DataFrame(step_results_prot,
                                        columns=['Time [sec]', 'Time [min]', 'θg [C]', 'θm [C]', 'c [J/kgC]', 'dθm [C]'])

    elif prot_type == 'fibcem_coating':

        for t in np.arange(0, t_min * 60, dt_sec):

            phi_factor = c_p * density_p * dp * Am_Vb / (specific_heat(mat, th_m) * density)

            th_m += dth_m

            step_results_prot.append([t, t / 60, fire_curve(t / 60), th_m, specific_heat(mat, th_m), dth_m, phi_factor])
            results_prot = pd.DataFrame(step_results_prot,
                                        columns=['Time [sec]', 'Time [min]', 'θg [C]', 'θm [C]', 'c [J/kgC]', 'dθm [C]', 'φ'
                                                 ])

            check = Am_Vb * 1000 * l_p / (dp * 10 ** -3 * specific_heat(mat, th_m) * density * (1+phi_factor/3)) * \
                    (fire_curve(t / 60) - th_m) * dt_sec - (np.exp(phi_factor / 10) - 1) * \
                    (fire_curve(t / 60 + dt_sec / 60) - fire_curve(t / 60))

            if check > 0:
                dth_m = check
            else: dth_m = 0

    if plot:
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
            name='Unprotected Member Temperature'), row=1, col=1)

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
            name='Protected Member Temperature'), row=1, col=2)

        fig4['layout']['yaxis']['title'] = 'Temperature [C]'
        fig4['layout']['xaxis']['title'] = 'Time [min]'
        fig4['layout']['xaxis2']['title'] = 'Time [min]'
        fig4.update_layout(title_text="Temperature-Time Curves")

        fig4.show()

    temp = list(results_prot['θm [C]'])[-1]

    temp1 = int(temp - temp%50)
    temp2 = temp1 + 50
    temp_diff = temp - temp1
    if temp2 > 400:
        f_red = 0
    else:
        f1 = strength_red[temp1]
        f2 = strength_red[temp2]
        f_red = interpolation(temp_diff, temp1, temp2, f1, f2)
    fy *= f_red
    E1 = stiff_red[temp1]
    if temp2 > 400:
        temp2 = 550
    E2 = stiff_red[temp2]
    E_red = interpolation(temp_diff, temp1, temp2, E1, E2)
    E *= E_red

    return fy, E

if __name__ == "__main__":
    fy, E = temperature()
    print(fy, E)
