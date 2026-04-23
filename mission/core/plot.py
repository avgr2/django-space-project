import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def generate_real_trajectory(result):
    theta = np.linspace(0, 2*np.pi, 1000)

    r_E = 149.597893e6
    r_J = 743e6

    x_E = r_E * np.cos(theta)
    y_E = r_E * np.sin(theta)

    x_J = r_J * np.cos(theta)
    y_J = r_J * np.sin(theta)

    a = result["a_2_km"]
    e = 1 - r_E / a

    theta_tr = np.linspace(0, np.pi, 500)
    r_tr = a * (1 - e**2) / (1 + e * np.cos(theta_tr))
    x_tr = r_tr * np.cos(theta_tr)
    y_tr = r_tr * np.sin(theta_tr)

    fig, ax = plt.subplots(figsize=(7, 7), facecolor='#0b1020')
    ax.set_facecolor('#0b1020')
    ax.plot(x_E / 1e6, y_E / 1e6, color='#38bdf8', label='Terre')
    ax.plot(x_J / 1e6, y_J / 1e6, color='#f59e0b', label='Jupiter')
    ax.plot(x_tr / 1e6, y_tr / 1e6, linestyle='--', color='#a78bfa', label='Trajectoire')
    ax.plot(0, 0, 'yo', markersize=10, label='Soleil')
    ax.legend(facecolor='#111a33', labelcolor='white')
    ax.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_edgecolor('#233')

    path = "trajectory.png"
    plt.savefig(path, facecolor=fig.get_facecolor())
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
