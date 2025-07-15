from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Doctor, Specialization
from appointments.models import TimeSlot
from datetime import date, timedelta

def doctor_list(request):
    doctors = Doctor.objects.filter(is_available=True).select_related('user', 'specialization')
    specializations = Specialization.objects.all()
    
    # Filter by specialization
    specialization_id = request.GET.get('specialization')
    if specialization_id:
        doctors = doctors.filter(specialization_id=specialization_id)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        doctors = doctors.filter(
            user__first_name__icontains=search_query
        ) | doctors.filter(
            user__last_name__icontains=search_query
        )
    
    # Pagination
    paginator = Paginator(doctors, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'specializations': specializations,
        'selected_specialization': specialization_id,
        'search_query': search_query,
    }
    return render(request, 'doctors/doctor_list.html', context)

def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id, is_available=True)
    
    # Get available time slots for the next 7 days
    today = date.today()
    available_dates = []
    
    for i in range(7):
        check_date = today + timedelta(days=i)
        time_slots = TimeSlot.objects.filter(
            doctor=doctor,
            date=check_date,
            is_available=True
        ).order_by('start_time')
        
        if time_slots.exists():
            available_dates.append({
                'date': check_date,
                'slots': time_slots
            })
    
    context = {
        'doctor': doctor,
        'available_dates': available_dates,
    }
    return render(request, 'doctors/doctor_detail.html', context)

@login_required
def get_available_slots(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    selected_date = request.GET.get('date')
    
    if not selected_date:
        return JsonResponse({'error': 'Date is required'}, status=400)
    
    try:
        selected_date = date.fromisoformat(selected_date)
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)
    
    time_slots = TimeSlot.objects.filter(
        doctor=doctor,
        date=selected_date,
        is_available=True
    ).order_by('start_time')
    
    slots_data = [
        {
            'id': slot.id,
            'start_time': slot.start_time.strftime('%H:%M'),
            'end_time': slot.end_time.strftime('%H:%M'),
        }
        for slot in time_slots
    ]
    
    return JsonResponse({'slots': slots_data})