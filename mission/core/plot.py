import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp


def generate_real_trajectory(result):
    mu_S = 13.27e10        # km³/s²
    r_E  = 149.597893e6   # km
    r_J  = 743e6          # km
    r_N  = 4.495e9        # km

    theta = np.linspace(0, 2 * np.pi, 1000)

    # ── Planetary orbits ──
    x_E, y_E = r_E * np.cos(theta), r_E * np.sin(theta)
    x_J, y_J = r_J * np.cos(theta), r_J * np.sin(theta)
    x_N, y_N = r_N * np.cos(theta), r_N * np.sin(theta)

    # ── Transfer ellipse Earth → Jupiter ──
    # Perihelion at (r_E, 0), aphelion at (-r_aph, 0) — theta from 0 to pi
    a = result["a_2_km"]
    e = 1 - r_E / a
    theta_tr = np.linspace(0, np.pi, 500)
    r_tr = a * (1 - e**2) / (1 + e * np.cos(theta_tr))
    x_tr = r_tr * np.cos(theta_tr)
    y_tr = r_tr * np.sin(theta_tr)

    # Jupiter sits at the aphelion end of the ellipse: approximately (-r_J, 0)
    jup_x, jup_y = x_tr[-1], y_tr[-1]

    # ── Outbound solar hyperbola Jupiter → Neptune ──
    # At (-r_J, 0), counterclockwise tangential = -y direction.
    # V_J_vec = (0, -V_J), V_R_incoming = (0, +V_R) [Jupiter overtakes probe].
    # Trailing-side flyby rotates V_R by alpha_3 toward -x (radially outward):
    #   V_R' = V_R * (-sin(alpha_3), +cos(alpha_3))
    #   V_S2 = V_J_vec + V_R' = (-V_R*sin(alpha_3), -V_J + V_R*cos(alpha_3))
    V_J_val     = result["V_J"]
    V_R         = result["V_R"]
    alpha_3_rad = result["alpha_3"] * np.pi / 180

    vx0 = -V_R * np.sin(alpha_3_rad)
    vy0 = -V_J_val + V_R * np.cos(alpha_3_rad)

    def eom(t, s):
        r = np.sqrt(s[0]**2 + s[1]**2)
        return [s[2], s[3], -mu_S * s[0] / r**3, -mu_S * s[1] / r**3]

    def reach_neptune(t, s):
        return np.sqrt(s[0]**2 + s[1]**2) - r_N
    reach_neptune.terminal = True
    reach_neptune.direction = 1

    t_eval = np.linspace(0, 7e8, 700)
    sol = solve_ivp(
        eom, [0, 7e8], [jup_x, jup_y, vx0, vy0],
        t_eval=t_eval, events=reach_neptune,
        rtol=1e-7, atol=1e3
    )
    x_out, y_out = sol.y[0], sol.y[1]

    # ── Plot ──
    fig, ax = plt.subplots(figsize=(8, 8), facecolor='#0b1020')
    ax.set_facecolor('#0b1020')
    ax.set_aspect('equal')

    s = 1e6  # scale: Mkm

    ax.plot(x_E / s, y_E / s, color='#38bdf8', lw=0.8, label='Earth orbit')
    ax.plot(x_J / s, y_J / s, color='#f59e0b', lw=0.8, label='Jupiter orbit')
    ax.plot(x_N / s, y_N / s, color='#818cf8', lw=0.8, label='Neptune orbit')
    ax.plot(x_tr / s, y_tr / s, '--', color='#a78bfa', lw=1.5, label='Transfer ellipse')
    ax.plot(x_out / s, y_out / s, color='#34d399', lw=1.5, label='Outbound hyperbola')

    ax.plot(0, 0, 'o', color='#fde68a', markersize=9, label='Sun')
    ax.plot(r_E / s, 0, 'o', color='#38bdf8', markersize=4)
    ax.plot(jup_x / s, jup_y / s, 'o', color='#f59e0b', markersize=6)

    ax.set_xlabel('x  (Mkm)', color='#90b8d8', fontsize=9)
    ax.set_ylabel('y  (Mkm)', color='#90b8d8', fontsize=9)
    ax.set_title('Pioneer 11 — Heliocentric Trajectory', color='#7dd3fc', pad=10)
    ax.legend(facecolor='#111a33', labelcolor='white', fontsize=8)
    ax.tick_params(colors='white')
    ax.grid(True, color='#1a2a3a', lw=0.4, linestyle=':')
    for spine in ax.spines.values():
        spine.set_edgecolor('#233344')

    path = "trajectory.png"
    plt.savefig(path, facecolor=fig.get_facecolor(), dpi=120, bbox_inches='tight')
    plt.close()
    return path


def generate_hyperbola(result):
    a = result["a_hJ_km"]
    e = result["e_hJ"]

    theta_max = np.arccos(-1 / e) * 0.98
    theta = np.linspace(-theta_max, theta_max, 500)
    r = a * (e**2 - 1) / (1 + e * np.cos(theta))

    x = r * np.cos(theta)
    y = r * np.sin(theta)

    fig, ax = plt.subplots(figsize=(7, 7), facecolor='#0b1020')
    ax.set_facecolor('#0b1020')
    ax.plot(x / 1e3, y / 1e3, color='#34d399')
    ax.plot(0, 0, 'yo', markersize=10, label='Jupiter')
    ax.legend(facecolor='#111a33', labelcolor='white')
    ax.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_edgecolor('#233')

    path = "hyperbola.png"
    plt.savefig(path, facecolor=fig.get_facecolor())
    plt.close()
    return path
