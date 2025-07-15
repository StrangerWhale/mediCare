from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from .models import Appointment, TimeSlot, MedicalRecord
from doctors.models import Doctor
from patients.models import Patient
from datetime import date, datetime

@login_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id, is_available=True)
    
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        messages.warning(request, 'Please complete your patient profile first.')
        return redirect('patient_profile_create')
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                appointment_date = request.POST.get('appointment_date')
                time_slot_id = request.POST.get('time_slot')
                appointment_type = request.POST.get('appointment_type')
                symptoms = request.POST.get('symptoms', '')
                
                # Get the time slot
                time_slot = get_object_or_404(TimeSlot, id=time_slot_id, doctor=doctor, is_available=True)
                
                # Create appointment
                appointment = Appointment.objects.create(
                    patient=patient,
                    doctor=doctor,
                    appointment_date=appointment_date,
                    appointment_time=time_slot.start_time,
                    appointment_type=appointment_type,
                    symptoms=symptoms,
                    status='pending'
                )
                
                # Mark time slot as unavailable
                time_slot.is_available = False
                time_slot.save()
                
                messages.success(request, 'Appointment booked successfully!')
                return redirect('appointment_detail', appointment_id=appointment.id)
                
        except Exception as e:
            messages.error(request, f'Error booking appointment: {str(e)}')
    
    context = {
        'doctor': doctor,
    }
    return render(request, 'appointments/book_appointment.html', context)

@login_required
def appointment_list(request):
    try:
        patient = request.user.patient
        appointments = Appointment.objects.filter(
            patient=patient
        ).select_related('doctor', 'doctor__user', 'doctor__specialization').order_by('-appointment_date', '-appointment_time')
        
        context = {
            'appointments': appointments,
        }
        return render(request, 'appointments/appointment_list.html', context)
    except Patient.DoesNotExist:
        messages.warning(request, 'Please complete your patient profile first.')
        return redirect('patient_profile_create')

@login_required
def appointment_detail(request, appointment_id):
    try:
        patient = request.user.patient
        appointment = get_object_or_404(
            Appointment, 
            id=appointment_id, 
            patient=patient
        )
        
        # Try to get medical record if appointment is completed
        medical_record = None
        if appointment.status == 'completed':
            try:
                medical_record = appointment.medical_record
            except MedicalRecord.DoesNotExist:
                pass
        
        context = {
            'appointment': appointment,
            'medical_record': medical_record,
        }
        return render(request, 'appointments/appointment_detail.html', context)
    except Patient.DoesNotExist:
        messages.warning(request, 'Please complete your patient profile first.')
        return redirect('patient_profile_create')

@login_required
def cancel_appointment(request, appointment_id):
    try:
        patient = request.user.patient
        appointment = get_object_or_404(
            Appointment, 
            id=appointment_id, 
            patient=patient,
            status__in=['pending', 'confirmed']
        )
        
        if request.method == 'POST':
            with transaction.atomic():
                # Update appointment status
                appointment.status = 'cancelled'
                appointment.save()
                
                # Make time slot available again
                try:
                    time_slot = TimeSlot.objects.get(
                        doctor=appointment.doctor,
                        date=appointment.appointment_date,
                        start_time=appointment.appointment_time
                    )
                    time_slot.is_available = True
                    time_slot.save()
                except TimeSlot.DoesNotExist:
                    pass
                
                messages.success(request, 'Appointment cancelled successfully!')
                return redirect('appointment_list')
        
        context = {
            'appointment': appointment,
        }
        return render(request, 'appointments/cancel_appointment.html', context)
        
    except Patient.DoesNotExist:
        messages.warning(request, 'Please complete your patient profile first.')
        return redirect('patient_profile_create')

def home(request):
    from doctors.models import Specialization
    
    # Get some statistics
    total_doctors = Doctor.objects.filter(is_available=True).count()
    total_specializations = Specialization.objects.count()
    
    # Get featured specializations
    featured_specializations = Specialization.objects.all()[:6]
    
    context = {
        'total_doctors': total_doctors,
        'total_specializations': total_specializations,
        'featured_specializations': featured_specializations,
    }
    return render(request, 'home.html', context)