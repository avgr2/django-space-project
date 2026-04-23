from django import forms


class TrajectoryForm(forms.Form):
    V_a = forms.FloatField(
        label="V_a — Vitesse au périgée après injection (km/s)",
        initial=15.850,
        min_value=10.0,
        max_value=30.0,
        widget=forms.NumberInput(attrs={"step": "0.001"}),
    )
    z_p = forms.FloatField(
        label="z_p — Altitude périgée Terre (km)",
        initial=229,
        min_value=150,
        max_value=2000,
        widget=forms.NumberInput(attrs={"step": "1"}),
    )
    z_J = forms.FloatField(
        label="z_J — Altitude périjove Jupiter (km)",
        initial=1000,
        min_value=100,
        max_value=200000,
        widget=forms.NumberInput(attrs={"step": "100"}),
    )
    fac = forms.FloatField(
        label="fac — Facteur géométrique swing-by",
        initial=0.54,
        min_value=0.0,
        max_value=2.0,
        widget=forms.NumberInput(attrs={"step": "0.01"}),
    )
