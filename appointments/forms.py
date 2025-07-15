from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['appointment_date', 'appointment_time', 'symptoms']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date', 'min': ''}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time'}),
            'symptoms': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe your symptoms or reason for visit'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set minimum date to today
        from datetime import date
        self.fields['appointment_date'].widget.attrs['min'] = date.today().strftime('%Y-%m-%d')