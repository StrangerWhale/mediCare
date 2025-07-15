from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from .models import Appointment, TimeSlot
from .forms import AppointmentForm
from doctors.models import Doctor
from datetime import date, datetime, timedelta, time
import json

@login_required
def book_appointment(request, doctor_id):
    try:
        patient = request.user.patient
    except:
        messages.error(request, 'You need to register as a patient first.')
        return redirect('patients:patient_register')
    
    doctor = get_object_or_404(Doctor, id=doctor_id, is_available=True)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.doctor = doctor
            
            # Check if slot is available
            existing_appointment = Appointment.objects.filter(
                doctor=doctor,
                appointment_date=appointment.appointment_date,
                appointment_time=appointment.appointment_time,
                status__in=['scheduled', 'confirmed']
            ).exists()
            
            if existing_appointment:
                messages.error(request, 'This time slot is not available.')
                return render(request, 'appointments/book_appointment.html', {
                    'form': form,
                    'doctor': doctor,
                })
            
            appointment.save()
            messages.success(request, 'Appointment booked successfully!')
            return redirect('appointments:my_appointments')
    else:
        form = AppointmentForm()
    
    # Get doctor's schedule
    schedules = doctor.schedules.filter(is_active=True)
    
    context = {
        'form': form,
        'doctor': doctor,
        'schedules': schedules,
    }
    return render(request, 'appointments/book_appointment.html', context)

@login_required
def my_appointments(request):
    try:
        patient = request.user.patient
    except:
        messages.error(request, 'You are not registered as a patient.')
        return redirect('home')
    
    appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date', '-appointment_time')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    
    context = {
        'appointments': appointments,
        'patient': patient,
        'status_filter': status_filter,
    }
    return render(request, 'appointments/my_appointments.html', context)

@login_required
def cancel_appointment(request, appointment_id):
    try:
        patient = request.user.patient
    except:
        messages.error(request, 'You are not registered as a patient.')
        return redirect('home')
    
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=patient)
    
    if appointment.status in ['completed', 'cancelled']:
        messages.error(request, 'Cannot cancel this appointment.')
        return redirect('appointments:my_appointments')
    
    # Check if appointment is at least 24 hours away
    appointment_datetime = datetime.combine(appointment.appointment_date, appointment.appointment_time)
    if appointment_datetime <= timezone.now() + timedelta(hours=24):
        messages.error(request, 'Cannot cancel appointment less than 24 hours before scheduled time.')
        return redirect('appointments:my_appointments')
    
    if request.method == 'POST':
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, 'Appointment cancelled successfully!')
        return redirect('appointments:my_appointments')
    
    context = {
        'appointment': appointment,
    }
    return render(request, 'appointments/cancel_appointment.html', context)

@login_required
def reschedule_appointment(request, appointment_id):
    try:
        patient = request.user.patient
    except:
        messages.error(request, 'You are not registered as a patient.')
        return redirect('home')
    
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=patient)
    
    if appointment.status in ['completed', 'cancelled']:
        messages.error(request, 'Cannot reschedule this appointment.')
        return redirect('appointments:my_appointments')
    
    if request.method == 'POST':
        new_date = request.POST.get('appointment_date')
        new_time = request.POST.get('appointment_time')
        
        # Check if new slot is available
        existing_appointment = Appointment.objects.filter(
            doctor=appointment.doctor,
            appointment_date=new_date,
            appointment_time=new_time,
            status__in=['scheduled', 'confirmed']
        ).exclude(id=appointment.id).exists()
        
        if existing_appointment:
            messages.error(request, 'This time slot is not available.')
        else:
            appointment.appointment_date = new_date
            appointment.appointment_time = new_time
            appointment.save()
            messages.success(request, 'Appointment rescheduled successfully!')
            return redirect('appointments:my_appointments')
    
    # Get doctor's schedule
    schedules = appointment.doctor.schedules.filter(is_active=True)
    
    context = {
        'appointment': appointment,
        'schedules': schedules,
    }
    return render(request, 'appointments/reschedule_appointment.html', context)

def get_available_slots(request, doctor_id, date):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    appointment_date = datetime.strptime(date, '%Y-%m-%d').date()
    
    # Get day of week
    day_name = appointment_date.strftime('%A').lower()
    
    # Get doctor's schedule for this day
    try:
        schedule = doctor.schedules.get(day_of_week=day_name, is_active=True)
    except:
        return JsonResponse({'slots': []})
    
    # Generate time slots (30-minute intervals)
    slots = []
    current_time = schedule.start_time
    end_time = schedule.end_time
    
    while current_time < end_time:
        # Check if slot is available
        existing_appointment = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=current_time,
            status__in=['scheduled', 'confirmed']
        ).exists()
        
        if not existing_appointment:
            slots.append({
                'time': current_time.strftime('%H:%M'),
                'display': current_time.strftime('%I:%M %p')
            })
        
        # Add 30 minutes
        current_time = (datetime.combine(date.today(), current_time) + timedelta(minutes=30)).time()
    
    return JsonResponse({'slots': slots})