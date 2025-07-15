from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Doctor, Specialization, DoctorSchedule

class DoctorRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    specialization = forms.ModelChoiceField(queryset=Specialization.objects.all(), required=True)
    license_number = forms.CharField(max_length=50, required=True)
    phone_number = forms.CharField(max_length=17, required=True)
    experience_years = forms.IntegerField(min_value=0, required=True)
    consultation_fee = forms.DecimalField(max_digits=10, decimal_places=2, required=True)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            Doctor.objects.create(
                user=user,
                specialization=self.cleaned_data['specialization'],
                license_number=self.cleaned_data['license_number'],
                phone_number=self.cleaned_data['phone_number'],
                experience_years=self.cleaned_data['experience_years'],
                consultation_fee=self.cleaned_data['consultation_fee'],
                bio=self.cleaned_data['bio']
            )
        return user

class DoctorScheduleForm(forms.ModelForm):
    class Meta:
        model = DoctorSchedule
        fields = ['day_of_week', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }