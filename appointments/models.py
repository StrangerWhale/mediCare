from django.db import models
from django.contrib.auth.models import User
from doctors.models import Doctor
from patients.models import Patient
from django.utils import timezone

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    symptoms = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    prescription = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['doctor', 'appointment_date', 'appointment_time']
        ordering = ['-appointment_date', '-appointment_time']
    
    def __str__(self):
        return f"{self.patient.user.username} with Dr. {self.doctor.name} on {self.appointment_date} at {self.appointment_time}"
    
    @property
    def is_past(self):
        from datetime import datetime, date, time
        appointment_datetime = datetime.combine(self.appointment_date, self.appointment_time)
        return appointment_datetime < timezone.now()

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='medical_record')
    diagnosis = models.TextField()
    treatment = models.TextField()
    prescription = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Medical Record - {self.patient.user.username} - {self.created_at.date()}"

class DiseaseSearch(models.Model):
    query = models.CharField(max_length=500)
    response = models.TextField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Search: {self.query[:50]}..."