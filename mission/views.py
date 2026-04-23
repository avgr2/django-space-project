from django.shortcuts import render
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

from .forms import TrajectoryForm
from .core.trajectory import compute_trajectory
from .core.plot import generate_real_trajectory, generate_hyperbola


def generate_pdf(request, result):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="pioneer11_report.pdf"'

    doc = SimpleDocTemplate(response)
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("Pioneer 11 — Trajectory Report", styles['Title']))
    content.append(Spacer(1, 20))

    try:
        traj = generate_real_trajectory(result)
        content.append(Image(traj, width=5*inch, height=5*inch))
        content.append(Spacer(1, 20))
    except Exception:
        pass

    try:
        hyp = generate_hyperbola(result)
        content.append(Image(hyp, width=5*inch, height=5*inch))
        content.append(Spacer(1, 20))
    except Exception:
        pass

    sections = [
        ("1 — Hyperbole départ (Terre)", [
            ("V_a", f"{result['V_a']} km/s"),
            ("C3", f"{result['C3']} km²/s²"),
            ("V∞", f"{result['V_inf']} km/s"),
            ("ΔV injection", f"{result['delta_V']} km/s"),
            ("φ* asymptote", f"{result['phi_star']}°"),
            ("Temps → SOI", result['t1_str']),
        ]),
        ("2 — Injection héliocentrique", [
            ("V_T", f"{result['V_T']} km/s"),
            ("V_P", f"{result['V_P']} km/s"),
            ("β", f"{result['beta']}°"),
            ("α", f"{result['alpha']}°"),
        ]),
        ("3 — Transfert Terre → Jupiter", [
            ("a₂", f"{result['a_2_Mkm']} Mkm"),
            ("e₂", str(result['e_2'])),
            ("φ₂", f"{result['phi_2']}°"),
            ("Temps de vol", result['t2_str']),
        ]),
        ("4 — Arrivée Jupiter", [
            ("V_J", f"{result['V_J']} km/s"),
            ("V_S1", f"{result['V_S1']} km/s"),
            ("V_R (V∞)", f"{result['V_R']} km/s"),
            ("γ", f"{result['gamma']}°"),
        ]),
        ("5 — Swing-by Jupiter", [
            ("z_J", f"{result['z_J']} km"),
            ("r_périjove", f"{result['r_pJ']} km"),
            ("e_h", str(result['e_hJ'])),
            ("δ déviation", f"{result['delta_deg']}°"),
            ("V_périjove", f"{result['V_pJ']} km/s"),
        ]),
        ("6 — Sortie swing-by", [
            ("α₃", f"{result['alpha_3']}°"),
            ("V_S2", f"{result['V_S2']} km/s"),
            ("E₂", f"{result['E2']} km²/s²"),
        ]),
        ("7 — Transfert Jupiter → Neptune", [
            ("Temps de vol", result['t3_str']),
        ]),
        ("Bilan de mission", [
            ("Terre → SOI", result['t1_str']),
            ("Terre → Jupiter", result['t2_str']),
            ("Jupiter → Neptune", result['t3_str']),
            ("TOTAL", f"{result['total_str']}  ({result['total_y']} ans)"),
        ]),
    ]

    for title, rows in sections:
        content.append(Paragraph(title, styles['Heading2']))
        for label, value in rows:
            content.append(Paragraph(f"{label} : {value}", styles['Normal']))
        content.append(Spacer(1, 10))

    doc.build(content)
    return response


def generate_pdf_view(request):
    form = TrajectoryForm(request.GET or None)
    if form.is_valid():
        result = compute_trajectory(
            V_a=form.cleaned_data["V_a"],
            z_p=form.cleaned_data["z_p"],
            z_J=form.cleaned_data["z_J"],
            fac=form.cleaned_data["fac"],
        )
    else:
        result = compute_trajectory()
    return generate_pdf(request, result)


def home(request):
    result = None
    error = None

    if request.method == "POST":
        form = TrajectoryForm(request.POST)
        if form.is_valid():
            try:
                result = compute_trajectory(
                    V_a=form.cleaned_data["V_a"],
                    z_p=form.cleaned_data["z_p"],
                    z_J=form.cleaned_data["z_J"],
                    fac=form.cleaned_data["fac"],
                )
            except Exception as e:
                error = str(e)
    else:
        form = TrajectoryForm()

    return render(request, "mission/home.html", {
        "form": form,
        "result": result,
        "error": error,
    })
