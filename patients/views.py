from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Patient
from appointments.models import Appointment
from django.db import transaction

@login_required
def patient_dashboard(request):
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        messages.warning(request, 'Please complete your patient profile.')
        return redirect('patient_profile_create')
    
    # Get recent appointments
    recent_appointments = Appointment.objects.filter(
        patient=patient
    ).select_related('doctor', 'doctor__user', 'doctor__specialization').order_by('-appointment_date', '-appointment_time')[:5]
    
    # Get upcoming appointments
    upcoming_appointments = Appointment.objects.filter(
        patient=patient,
        status__in=['pending', 'confirmed'],
        appointment_date__gte=date.today()
    ).select_related('doctor', 'doctor__user', 'doctor__specialization').order_by('appointment_date', 'appointment_time')[:3]
    
    context = {
        'patient': patient,
        'recent_appointments': recent_appointments,
        'upcoming_appointments': upcoming_appointments,
    }
    return render(request, 'patients/dashboard.html', context)

@login_required
def patient_profile(request):
    try:
        patient = request.user.patient
        return render(request, 'patients/profile.html', {'patient': patient})
    except Patient.DoesNotExist:
        messages.warning(request, 'Please complete your patient profile.')
        return redirect('patient_profile_create')

@login_required
def patient_profile_create(request):
    if hasattr(request.user, 'patient'):
        return redirect('patient_profile')
    
    if request.method == 'POST':
        # Handle form submission
        try:
            with transaction.atomic():
                patient = Patient.objects.create(
                    user=request.user,
                    date_of_birth=request.POST.get('date_of_birth'),
                    gender=request.POST.get('gender'),
                    phone=request.POST.get('phone'),
                    address=request.POST.get('address'),
                    blood_group=request.POST.get('blood_group', ''),
                    emergency_contact=request.POST.get('emergency_contact'),
                    medical_history=request.POST.get('medical_history', ''),
                    allergies=request.POST.get('allergies', ''),
                )
                messages.success(request, 'Profile created successfully!')
                return redirect('patient_dashboard')
        except Exception as e:
            messages.error(request, f'Error creating profile: {str(e)}')
    
    return render(request, 'patients/profile_create.html')

def patient_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Please complete your profile.')
            return redirect('patient_profile_create')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

from datetime import date