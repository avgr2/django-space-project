from math import cos, asin, sin, sinh, pi, sqrt, acosh, acos
from scipy import integrate as sci_int


def seconds_to_readable(seconds):
    minute = 60
    hour   = 60 * minute
    day    = 24 * hour
    month  = 30 * day
    year   = 365 * day

    years   = seconds // year;  seconds %= year
    months  = seconds // month; seconds %= month
    days    = seconds // day;   seconds %= day
    hours   = seconds // hour;  seconds %= hour
    minutes = seconds // minute; seconds %= minute

    parts = []
    if years:   parts.append(f"{int(years)} y")
    if months:  parts.append(f"{int(months)} m")
    if days:    parts.append(f"{int(days)} day")
    if hours:   parts.append(f"{int(hours)} h")
    if minutes: parts.append(f"{int(minutes)} min")
    if seconds or not parts: parts.append(f"{int(seconds)} s")
    return " ".join(parts)


def compute_trajectory(V_a=15.850, z_p=229, z_J=1000, fac=0.54):
    # --- 1) Hyperbole de départ (Terre) ---
    mu_E  = 398600.4
    R_E   = 6378
    r     = R_E + z_p
    R_is  = 900000
    i     = 3.1 * pi / 180

    C3       = V_a**2 - 2 * mu_E / r
    V_inf    = sqrt(C3)
    a_E      = mu_E / C3
    e_E      = r / a_E + 1
    phi_star = acos(1 / e_E)
    V_circ   = sqrt(mu_E / r)
    delta_V  = V_a - V_circ

    phi_soi = acosh((R_is / a_E + 1) / e_E)
    t1      = a_E * sqrt(a_E / mu_E) * (e_E * sinh(phi_soi) - phi_soi)

    # --- 2) Injection héliocentrique ---
    mu_S = 13.27e10
    SE   = 149.597893e6

    V_T   = sqrt(mu_S / SE)
    beta  = asin(V_T / V_inf * sin(i))
    alpha = pi - beta - i
    V_P   = sqrt(V_T**2 + V_inf**2 - 2 * V_T * V_inf * cos(alpha))
    E     = V_P**2 / 2 - mu_S / SE

    # --- 3) Transfert Terre → Jupiter ---
    SJ   = 743e6
    a_2  = -mu_S / (2 * E)
    r_a2 = 2 * a_2 - SE
    e_2  = (r_a2 - SE) / (r_a2 + SE)

    phi_2 = acos((1 - SJ / a_2) / e_2)
    t2    = sqrt(a_2**3 / mu_S) * (phi_2 - e_2 * sin(phi_2))

    # --- 4) Vitesse relative à Jupiter ---
    V_J   = sqrt(mu_S / SJ)
    V_S1  = sqrt(2 * (mu_S / SJ - mu_S / (2 * a_2)))
    gamma = acos(V_P * SE / (V_S1 * SJ))
    V_R   = sqrt(V_J**2 + V_S1**2 - 2 * V_J * V_S1 * cos(gamma))

    # --- 5) Survol de Jupiter ---
    mu_J    = 126.5e6
    R_J     = 71400
    r_pJ    = R_J + z_J

    V_inf_J = V_R
    e_hJ    = 1 + r_pJ * V_inf_J**2 / mu_J
    delta   = 2 * asin(1 / e_hJ)
    V_pJ    = sqrt(V_inf_J**2 + 2 * mu_J / r_pJ)

    # --- 6) Sortie swing-by ---
    alpha_3 = gamma + fac * delta
    V_S2    = sqrt(V_R**2 + V_J**2 - 2 * V_R * V_J * cos(alpha_3))

    # --- 7) Transfert Jupiter → Neptune ---
    SN = 4.495e9
    E2 = V_S2**2 / 2 - mu_S / SJ

    def integrand_hyp(r_):
        v2 = 2 * (E2 + mu_S / r_)
        return 1 / sqrt(v2) if v2 > 0 else 1e10

    t3, _ = sci_int.quad(integrand_hyp, SJ, SN)

    total   = t1 + t2 + t3
    total_y = total / (365 * 86400)

    # Raw values kept for plots
    a_hJ = mu_J / V_inf_J**2

    return {
        # Input params (for PDF link passthrough)
        "z_p":        z_p,
        "fac":        fac,
        # Phase 1
        "V_a":        round(V_a, 3),
        "C3":         round(C3, 2),
        "V_inf":      round(V_inf, 3),
        "delta_V":    round(delta_V, 3),
        "phi_star":   round(phi_star * 180 / pi, 2),
        "t1_str":     seconds_to_readable(t1),
        # Phase 2
        "V_T":        round(V_T, 3),
        "V_P":        round(V_P, 3),
        "beta":       round(beta * 180 / pi, 2),
        "alpha":      round(alpha * 180 / pi, 2),
        # Phase 3
        "a_2_Mkm":    round(a_2 / 1e6, 2),
        "a_2_km":     a_2,
        "e_2":        round(e_2, 5),
        "phi_2":      round(phi_2 * 180 / pi, 2),
        "t2_str":     seconds_to_readable(t2),
        # Phase 4
        "V_J":        round(V_J, 3),
        "V_S1":       round(V_S1, 3),
        "V_R":        round(V_R, 3),
        "gamma":      round(gamma * 180 / pi, 2),
        # Phase 5
        "z_J":        z_J,
        "r_pJ":       r_pJ,
        "e_hJ":       round(e_hJ, 4),
        "a_hJ_km":    a_hJ,
        "delta_deg":  round(delta * 180 / pi, 2),
        "V_pJ":       round(V_pJ, 2),
        # Phase 6
        "alpha_3":    round(alpha_3 * 180 / pi, 2),
        "V_S2":       round(V_S2, 3),
        "E2":         round(E2, 2),
        # Phase 7
        "t3_str":     seconds_to_readable(t3),
        # Totaux
        "total_str":  seconds_to_readable(total),
        "total_y":    round(total_y, 4),
    }
