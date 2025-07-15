from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Patient

class PatientRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    gender = forms.ChoiceField(choices=Patient.GENDER_CHOICES, required=True)
    phone_number = forms.CharField(max_length=17, required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    blood_group = forms.ChoiceField(choices=Patient.BLOOD_GROUP_CHOICES, required=False)
    emergency_contact_name = forms.CharField(max_length=100, required=True)
    emergency_contact_phone = forms.CharField(max_length=17, required=True)
    medical_history = forms.CharField(widget=forms.Textarea, required=False)
    allergies = forms.CharField(widget=forms.Textarea, required=False)
    current_medications = forms.CharField(widget=forms.Textarea, required=False)
    
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
            Patient.objects.create(
                user=user,
                date_of_birth=self.cleaned_data['date_of_birth'],
                gender=self.cleaned_data['gender'],
                phone_number=self.cleaned_data['phone_number'],
                address=self.cleaned_data['address'],
                blood_group=self.cleaned_data['blood_group'],
                emergency_contact_name=self.cleaned_data['emergency_contact_name'],
                emergency_contact_phone=self.cleaned_data['emergency_contact_phone'],
                medical_history=self.cleaned_data['medical_history'],
                allergies=self.cleaned_data['allergies'],
                current_medications=self.cleaned_data['current_medications']
            )
        return user

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['phone_number', 'address', 'blood_group', 'emergency_contact_name', 
                 'emergency_contact_phone', 'medical_history', 'allergies', 'current_medications']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'medical_history': forms.Textarea(attrs={'rows': 4}),
            'allergies': forms.Textarea(attrs={'rows': 3}),
            'current_medications': forms.Textarea(attrs={'rows': 3}),
        }