from django.contrib import admin
from .models import Doctor, Specialization, DoctorSchedule

@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user', 'specialization', 'license_number', 'phone_number', 'experience_years', 'consultation_fee', 'is_available']
    list_filter = ['specialization', 'is_available', 'experience_years']
    search_fields = ['user__first_name', 'user__last_name', 'license_number', 'phone_number']
    readonly_fields = ['created_at']

@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'day_of_week', 'start_time', 'end_time', 'is_active']
    list_filter = ['day_of_week', 'is_active']
    search_fields = ['doctor__user__first_name', 'doctor__user__last_name']