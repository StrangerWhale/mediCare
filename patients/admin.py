from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'gender', 'phone_number', 'blood_group', 'age']
    list_filter = ['gender', 'blood_group', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'phone_number', 'emergency_contact_name']
    readonly_fields = ['created_at', 'age']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Personal Information', {
            'fields': ('date_of_birth', 'gender', 'phone_number', 'address', 'blood_group')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone')
        }),
        ('Medical Information', {
            'fields': ('medical_history', 'allergies', 'current_medications')
        }),
        ('System Information', {
            'fields': ('created_at', 'age'),
            'classes': ('collapse',)
        })
    )