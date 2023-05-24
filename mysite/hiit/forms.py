from django import forms
from .models import Workout

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['name', 'warm_up_duration', 'high_intensity_duration', 'recovery_duration', 'number_of_intervals']
