from django import forms

class TrajectoryForm(forms.Form):
    z_p = forms.FloatField(label="Altitude (km)", initial=200)
    delta_v = forms.FloatField(label="Delta V (km/s)", initial=7.17)
    angle_deg = forms.FloatField(label="Angle (deg)", initial=16.7)