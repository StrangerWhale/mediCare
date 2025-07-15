from django.contrib import admin
from .models import Appointment, TimeSlot, MedicalRecord

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'appointment_date', 'appointment_time', 'status', 'created_at']
    list_filter = ['status', 'appointment_date', 'doctor__specialization', 'created_at']
    search_fields = ['patient__user__first_name', 'patient__user__last_name', 'doctor__user__first_name', 'doctor__user__last_name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'appointment_date'
    
    fieldsets = (
        ('Appointment Information', {
            'fields': ('patient', 'doctor', 'appointment_date', 'appointment_time', 'status')
        }),
        ('Medical Information', {
            'fields': ('symptoms', 'notes', 'prescription', 'follow_up_date')
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'date', 'start_time', 'end_time', 'is_available']
    list_filter = ['is_available', 'date', 'doctor']
    search_fields = ['doctor__user__first_name', 'doctor__user__last_name']
    date_hierarchy = 'date'

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'appointment', 'created_at']
    list_filter = ['created_at', 'doctor__specialization']
    search_fields = ['patient__user__first_name', 'patient__user__last_name', 'doctor__user__first_name', 'doctor__user__last_name', 'diagnosis']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Record Information', {
            'fields': ('patient', 'doctor', 'appointment')
        }),
        ('Medical Details', {
            'fields': ('diagnosis', 'treatment', 'prescription', 'notes', 'next_visit_date')
        }),
        ('System Information', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )