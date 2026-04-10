from math import cos, asin, sin, sinh, pi, sqrt, acosh, acos
 

# =========================
# UTILS
# =========================

def seconds_to_readable(seconds):
    minute = 60
    hour = 60 * minute
    day = 24 * hour
    month = 30 * day
    year = 365 * day

    years = seconds // year
    seconds %= year

    months = seconds // month
    seconds %= month

    days = seconds // day
    seconds %= day

    hours = seconds // hour
    seconds %= hour

    minutes = seconds // minute
    seconds %= minute

    parts = []

    # YEARS
    if years:
        parts.append(f"{int(years)} y")

    # MONTHS
    if months:
        parts.append(f"{int(months)} m")

    # DAYS
    if days:
        parts.append(f"{int(days)} day")

    # HOURS
    if hours:
        parts.append(f"{int(hours)} h")

    # MINUTES
    if minutes:
        parts.append(f"{int(minutes)} min")

    # SECONDS
    if seconds or not parts:
        parts.append(f"{int(seconds)} ")

    return " ".join(parts)


# =========================
# MAIN COMPUTATION
# =========================

def compute_trajectory(
    z_p=200,
    delta_v=7.17,
    angle_deg=16.7,
):
    """
    Calcule une trajectoire Terre -> Jupiter.

    Paramètres
    ----------
    z_p : float
        altitude initiale (km)
    delta_v : float
        delta V injection (km/s)
    angle_deg : float
        angle entre V_E et V_inf (deg)

    Returns
    -------
    dict
        tous les résultats physiques
    """

    # CONSTANTES
    mu_E = 398600.4
    R_E = 6378

    mu_S = 13.27E10
    r_ES = 150E6
    SJ = 778.6E6

    mu_J = 126.5E6
    R_J = 71400

    # =========================
    # EARTH ESCAPE
    # =========================

    r = R_E + z_p
    V_200 = sqrt(mu_E / r)
    V_p = delta_v + V_200

    a = mu_E / (V_p**2 - 2 * mu_E / r)
    V_inf = sqrt(mu_E / a)
    e = 1 + r / a

    R_IS = 900000
    E = acosh((1 + R_IS / a) / e)
    t = sqrt(a**3 / mu_E) * (e * sinh(E) - E)

    # =========================
    # HELIOCENTRIC FRAME
    # =========================

    angle = angle_deg * pi / 180

    V_E = sqrt(mu_S / r_ES)
    V_S0 = sqrt(V_E**2 + V_inf**2 + 2 * V_E * V_inf * cos(angle))

    # =========================
    # TRANSFER ORBIT
    # =========================

    SE = r_ES
    a2 = - mu_S / (2 * ((V_S0**2) / 2 - (mu_S / SE)))

    V_S1 = sqrt(2 * (-mu_S / (2 * a2) + mu_S / SJ))

    gamma = acos((V_S0 * SE) / (V_S1 * SJ))

    V_J = sqrt(mu_S / SJ)

    V_inf1 = sqrt(V_S1**2 + V_J**2 - 2 * V_S1 * V_J * cos(gamma))

    # =========================
    # TRANSFER TIME
    # =========================

    e2 = 1 - SE/a2
    E2 = acos((1 - SJ/a2)/e2)

    t2 = sqrt(a2**3 / mu_S) * (E2 - e2 * sin(E2))

    # =========================
    # JUPITER FLYBY
    # =========================

    a_H = mu_J / V_inf1**2

    r_PH = 1.65 * R_J
    e_H = 1 + r_PH / a_H

    phi_H = acos(1 / e_H)

    alpha1 = asin(V_S1 / V_inf1 * sin(gamma))
    alpha2 = pi - 2 * phi_H - alpha1

    # =========================
    # OUTPUT
    # =========================

    return {

        "raw": {
            "earth_escape": {
                "r": r,
                "V_200": V_200,
                "V_p": V_p,
                "V_inf": V_inf,
                "a": a,
                "e": e,
                "t_escape": t,
            },
            "heliocentric": {
                "V_E": V_E,
                "V_S0": V_S0,
            },
            "transfer": {
                "a2": a2,
                "V_S1": V_S1,
                "gamma_rad": gamma,
                "gamma_deg": gamma * 180 / pi,
                "V_J": V_J,
                "V_inf1": V_inf1,
                "t_transfer": t2,
            },
            "jupiter_flyby": {
                "a_H": a_H,
                "r_PH": r_PH,
                "e_H": e_H,
                "phi_H_rad": phi_H,
                "phi_H_deg": phi_H * 180 / pi,
                "alpha1_deg": alpha1 * 180 / pi,
                "alpha2_deg": alpha2 * 180 / pi,
            }
        },

        "display": {

        
            "earth_escape": {
                "r": rf"$r = {round(r)}\ \mathrm{{km}}$",
                "V_200": rf"$V_{{200}} = {round(V_200,2)}\ \mathrm{{km/s}}$",
                "V_p": rf"$V_p = {round(V_p,2)}\ \mathrm{{km/s}}$",
                "V_inf": rf"$V_{{\infty}} = {round(V_inf,2)}\ \mathrm{{km/s}}$",
                "a": rf"$a = {round(a)}\ \mathrm{{km}}$",
                "e": rf"$e = {round(e,4)}$",
                "line": "-----------------------------------------------------",
                "t_escape": rf"$t_{{escape}} = {round(t)} \mathrm{{s}}$",
                "t_escape2": rf"$t_{{escape}} = {seconds_to_readable(round(t))}$"
            },
            "heliocentric": {
                "V_E": rf"$V_E = {round(V_E,2)}\ \mathrm{{km/s}}$",
                "V_S0": rf"$V_{{S0}} = {(round(V_S0, 2))}\ \mathrm{{km/s}} $",
            },
            "transfer": {
                "a2": rf"$a_T = {round(a2)}\ \mathrm{{km}} $",
                "V_S1": rf"$V_{{S1}} = {round(V_S1,2)}\ \mathrm{{km/s}} $",
                "gamma_rad": rf"$\gamma = {round(gamma,3)}\ \mathrm{{rad}} $",
                "gamma_deg": rf"$\gamma = {round(gamma * 180 / pi, 2)} \mathrm{{^\circ}} $",
                "V_J": rf"$V_{{J}} = {round(V_J,2)}\ \mathrm{{km/s}} $",
                "V_inf1": rf"$V_{{\infty 1}} = {round(V_inf1,2)}\ \mathrm{{km/s}} $",
                "line": "-----------------------------------------------------",
                "t_transfer": rf"$t_{{transfer}} = {round(t2)} \mathrm{{s}}$",
                "t_transfer_readable": rf"$t_{{transfer}} = {seconds_to_readable(round(t2))} \mathrm{{s}}$",
            },
            "jupiter_flyby": {
                "a_H": rf"$a_H = {round(a_H)}\ \mathrm{{km}} $",
                "r_PH": rf"$r_{{PH}} = {round(r_PH)}\ \mathrm{{km}}$",
                "e_H": rf"$e_H = {round(e_H,4)}$",
                "phi_H_rad": rf"$\varphi = {round(phi_H, 4)}\ \mathrm{{rad}}$",
                "phi_H_deg": rf"$\varphi = {round(phi_H * 180 / pi, 2)} \mathrm{{^\circ}}$",
                "alpha1_deg": rf"$\alpha_1 = {round(alpha1 * 180 / pi,2)} \mathrm{{^\circ}}$",
                "alpha2_deg": rf"$\alpha_2 = {round(alpha2 * 180 / pi,2)} \mathrm{{^\circ}}$",
            }
        },
        
    }