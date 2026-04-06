import matplotlib
matplotlib.use('Agg')  # Backend serveur sans GUI
import matplotlib.pyplot as plt
import numpy as np

def generate_real_trajectory(result):
    theta = np.linspace(0, 2*np.pi, 1000)

    r_E = 150e6
    r_J = 778.6e6

    x_E = r_E * np.cos(theta)
    y_E = r_E * np.sin(theta)

    x_J = r_J * np.cos(theta)
    y_J = r_J * np.sin(theta)

    a = result["transfer"]["a2"]
    e = 1 - r_E / a

    theta_tr = np.linspace(0, np.pi, 500)
    r = a * (1 - e**2) / (1 + e * np.cos(theta_tr))

    x_tr = r * np.cos(theta_tr)
    y_tr = r * np.sin(theta_tr)

    plt.figure()
    plt.plot(x_E, y_E)
    plt.plot(x_J, y_J)
    plt.plot(x_tr, y_tr, linestyle="--")

    path = "trajectory.png"
    plt.savefig(path)
    plt.close()

    return path


def generate_hyperbola(result):
    theta = np.linspace(-np.pi/2, np.pi/2, 500)

    a = result["raw"]["jupiter_flyby"]["a_H"]
    e = result["raw"]["jupiter_flyby"]["e_H"]

    r = a * (e**2 - 1) / (1 + e * np.cos(theta))

    x = r * np.cos(theta)
    y = r * np.sin(theta)

    plt.figure()
    plt.plot(x, y)

    path = "hyperbola.png"
    plt.savefig(path)
    plt.close()

    return path