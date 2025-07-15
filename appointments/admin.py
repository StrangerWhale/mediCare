from django.contrib import admin
from .models import Appointment, MedicalRecord, TimeSlot

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'appointment_date', 'appointment_time', 'status', 'appointment_type']
    list_filter = ['status', 'appointment_type', 'appointment_date', 'doctor__specialization']
    search_fields = ['patient__user__first_name', 'patient__user__last_name', 'doctor__user__first_name', 'doctor__user__last_name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'appointment_date'

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'diagnosis', 'follow_up_required', 'follow_up_date']
    list_filter = ['follow_up_required', 'created_at']
    search_fields = ['appointment__patient__user__first_name', 'appointment__patient__user__last_name', 'diagnosis']
    readonly_fields = ['created_at']

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'date', 'start_time', 'end_time', 'is_available']
    list_filter = ['is_available', 'date', 'doctor__specialization']
    search_fields = ['doctor__user__first_name', 'doctor__user__last_name']