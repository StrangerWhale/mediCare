from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .models import Patient
from .forms import PatientRegistrationForm, PatientProfileForm
from appointments.models import Appointment, MedicalRecord
from datetime import date

def patient_register(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Patient registration successful!')
            return redirect('patients:patient_dashboard')
    else:
        form = PatientRegistrationForm()
    
    return render(request, 'patients/patient_register.html', {'form': form})

@login_required
def patient_profile(request):
    try:
        patient = request.user.patient
    except:
        messages.error(request, 'You are not registered as a patient.')
        return redirect('home')
    
    context = {
        'patient': patient,
    }
    return render(request, 'patients/patient_profile.html', context)

@login_required
def patient_dashboard(request):
    try:
        patient = request.user.patient
    except:
        messages.error(request, 'You are not registered as a patient.')
        return redirect('home')
    
    today = date.today()
    upcoming_appointments = Appointment.objects.filter(
        patient=patient,
        appointment_date__gte=today,
        status__in=['scheduled', 'confirmed']
    ).order_by('appointment_date', 'appointment_time')[:5]
    
    recent_appointments = Appointment.objects.filter(
        patient=patient,
        status='completed'
    ).order_by('-appointment_date', '-appointment_time')[:3]
    
    total_appointments = Appointment.objects.filter(patient=patient).count()
    
    context = {
        'patient': patient,
        'upcoming_appointments': upcoming_appointments,
        'recent_appointments': recent_appointments,
        'total_appointments': total_appointments,
    }
    return render(request, 'patients/patient_dashboard.html', context)

@login_required
def medical_records(request):
    try:
        patient = request.user.patient
    except:
        messages.error(request, 'You are not registered as a patient.')
        return redirect('home')
    
    records = MedicalRecord.objects.filter(patient=patient).order_by('-created_at')
    
    context = {
        'patient': patient,
        'records': records,
    }
    return render(request, 'patients/medical_records.html', context)

@login_required
def edit_profile(request):
    try:
        patient = request.user.patient
    except:
        messages.error(request, 'You are not registered as a patient.')
        return redirect('home')
    
    if request.method == 'POST':
        form = PatientProfileForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('patients:patient_profile')
    else:
        form = PatientProfileForm(instance=patient)
    
    context = {
        'form': form,
        'patient': patient,
    }
    return render(request, 'patients/edit_profile.html', context)