# Create your views here.
from django.shortcuts import render
from .forms import TrajectoryForm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from django.http import HttpResponse
from .core.trajectory import compute_trajectory
from .core.plot import generate_real_trajectory, generate_hyperbola


def generate_pdf(request, result):
    print(result.keys())

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="trajectory_report.pdf"'

    doc = SimpleDocTemplate(response)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("Trajectory Report", styles['Title']))
    content.append(Spacer(1, 20))

    # Graphs
    traj = generate_real_trajectory(result)
    hyp = generate_hyperbola(result)

    content.append(Image(traj, width=5*inch, height=5*inch))
    content.append(Spacer(1, 20))

    content.append(Image(hyp, width=5*inch, height=5*inch))
    content.append(Spacer(1, 20))


    # Results
    for section, values in result.items():
        content.append(Paragraph(section.upper(), styles['Heading2']))
        for key, value in values.items():
            content.append(Paragraph(str(value), styles['Normal']))
        content.append(Spacer(1, 10))

    doc.build(content)

    return response


def generate_pdf_view(request):

    form = TrajectoryForm(request.GET or None)

    if form.is_valid():
        result = compute_trajectory(
            form.cleaned_data["z_p"],
            form.cleaned_data["delta_v"],
            form.cleaned_data["angle_deg"]
        )
    else:
        result = compute_trajectory()

    # ✅ on passe DIRECTEMENT result
    return generate_pdf(request, result)

def home(request):

    result = None

    if request.method == "POST":
        form = TrajectoryForm(request.POST)

        if form.is_valid():

            z_p = form.cleaned_data["z_p"]
            delta_v = form.cleaned_data["delta_v"]
            angle = form.cleaned_data["angle_deg"]

            # ✅ 1. calcul physique
            result_raw = compute_trajectory(z_p, delta_v, angle)

            # ✅ 2. données pour HTML
            result = result_raw["display"]

            # (optionnel) trajectoire pour PDF/debug
            traj = generate_real_trajectory(result_raw["raw"])

    else:
        form = TrajectoryForm()

    return render(request, "mission/home.html", {
        "form": form,
        "result": result
    })