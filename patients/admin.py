from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'gender', 'phone', 'blood_group']
    list_filter = ['gender', 'blood_group', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'phone']
    readonly_fields = ['created_at', 'updated_at']