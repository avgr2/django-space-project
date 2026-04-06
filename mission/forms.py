from django import forms

class TrajectoryForm(forms.Form):
    z_p = forms.FloatField(label="Altitude (km)")
    delta_v = forms.FloatField(label="Delta V (km/s)")
    angle_deg = forms.FloatField(label="Angle (deg)", initial=16.7)