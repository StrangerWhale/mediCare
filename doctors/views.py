from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import Doctor, Specialization, DoctorSchedule
from .forms import DoctorRegistrationForm, DoctorScheduleForm
from appointments.models import Appointment
from datetime import date, datetime, timedelta

def doctor_list(request):
    doctors = Doctor.objects.filter(is_available=True).select_related('specialization', 'user')
    specializations = Specialization.objects.all()
    
    # Filter by specialization
    specialization_id = request.GET.get('specialization')
    if specialization_id:
        doctors = doctors.filter(specialization_id=specialization_id)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        doctors = doctors.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(specialization__name__icontains=search_query)
        )
    
    context = {
        'doctors': doctors,
        'specializations': specializations,
        'selected_specialization': specialization_id,
        'search_query': search_query,
    }
    return render(request, 'doctors/doctor_list.html', context)

def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id, is_available=True)
    schedules = doctor.schedules.filter(is_active=True)
    
    context = {
        'doctor': doctor,
        'schedules': schedules,
    }
    return render(request, 'doctors/doctor_detail.html', context)

def doctor_register(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Doctor registration successful!')
            return redirect('doctors:doctor_dashboard')
    else:
        form = DoctorRegistrationForm()
    
    return render(request, 'doctors/doctor_register.html', {'form': form})

@login_required
def doctor_dashboard(request):
    try:
        doctor = request.user.doctor
    except:
        messages.error(request, 'You are not registered as a doctor.')
        return redirect('home')
    
    today = date.today()
    upcoming_appointments = Appointment.objects.filter(
        doctor=doctor,
        appointment_date__gte=today,
        status__in=['scheduled', 'confirmed']
    ).order_by('appointment_date', 'appointment_time')[:5]
    
    total_appointments = Appointment.objects.filter(doctor=doctor).count()
    today_appointments = Appointment.objects.filter(
        doctor=doctor,
        appointment_date=today
    ).count()
    
    context = {
        'doctor': doctor,
        'upcoming_appointments': upcoming_appointments,
        'total_appointments': total_appointments,
        'today_appointments': today_appointments,
    }
    return render(request, 'doctors/doctor_dashboard.html', context)

@login_required
def manage_schedule(request):
    try:
        doctor = request.user.doctor
    except:
        messages.error(request, 'You are not registered as a doctor.')
        return redirect('home')
    
    if request.method == 'POST':
        form = DoctorScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.doctor = doctor
            schedule.save()
            messages.success(request, 'Schedule added successfully!')
            return redirect('doctors:manage_schedule')
    else:
        form = DoctorScheduleForm()
    
    schedules = doctor.schedules.all()
    
    context = {
        'form': form,
        'schedules': schedules,
        'doctor': doctor,
    }
    return render(request, 'doctors/manage_schedule.html', context)

@login_required
def doctor_appointments(request):
    try:
        doctor = request.user.doctor
    except:
        messages.error(request, 'You are not registered as a doctor.')
        return redirect('home')
    
    appointments = Appointment.objects.filter(doctor=doctor).order_by('-appointment_date', '-appointment_time')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    
    # Filter by date
    date_filter = request.GET.get('date')
    if date_filter:
        appointments = appointments.filter(appointment_date=date_filter)
    
    context = {
        'appointments': appointments,
        'doctor': doctor,
        'status_filter': status_filter,
        'date_filter': date_filter,
    }
    return render(request, 'doctors/doctor_appointments.html', context)

@login_required
def update_appointment(request, appointment_id):
    try:
        doctor = request.user.doctor
    except:
        messages.error(request, 'You are not registered as a doctor.')
        return redirect('home')
    
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        notes = request.POST.get('notes')
        prescription = request.POST.get('prescription')
        
        appointment.status = status
        appointment.notes = notes
        appointment.prescription = prescription
        appointment.save()
        
        messages.success(request, 'Appointment updated successfully!')
        return redirect('doctors:doctor_appointments')
    
    context = {
        'appointment': appointment,
        'doctor': doctor,
    }
    return render(request, 'doctors/update_appointment.html', context)