#!/usr/bin/env python
import os
import sys
import django
from datetime import date, time, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicare_1.settings')
django.setup()

from django.contrib.auth.models import User
from doctors.models import Doctor, Specialization, DoctorSchedule
from patients.models import Patient
from appointments.models import TimeSlot

def create_sample_data():
    print("Creating sample data...")
    
    # Create specializations
    specializations_data = [
        {'name': 'Cardiology', 'description': 'Heart and cardiovascular system specialists'},
        {'name': 'Dermatology', 'description': 'Skin, hair, and nail specialists'},
        {'name': 'Pediatrics', 'description': 'Medical care for infants, children, and adolescents'},
        {'name': 'Orthopedics', 'description': 'Bone, joint, and muscle specialists'},
        {'name': 'Neurology', 'description': 'Brain and nervous system specialists'},
        {'name': 'General Medicine', 'description': 'Primary healthcare and general medical conditions'},
    ]
    
    for spec_data in specializations_data:
        specialization, created = Specialization.objects.get_or_create(
            name=spec_data['name'],
            defaults={'description': spec_data['description']}
        )
        if created:
            print(f"Created specialization: {specialization.name}")
    
    # Create sample doctors
    doctors_data = [
        {
            'username': 'dr_smith',
            'first_name': 'John',
            'last_name': 'Smith',
            'email': 'dr.smith@medicare.com',
            'specialization': 'Cardiology',
            'license_number': 'MD001',
            'phone': '+1-555-0101',
            'experience_years': 15,
            'consultation_fee': 150.00,
            'bio': 'Experienced cardiologist with expertise in heart disease prevention and treatment.'
        },
        {
            'username': 'dr_johnson',
            'first_name': 'Sarah',
            'last_name': 'Johnson',
            'email': 'dr.johnson@medicare.com',
            'specialization': 'Dermatology',
            'license_number': 'MD002',
            'phone': '+1-555-0102',
            'experience_years': 12,
            'consultation_fee': 120.00,
            'bio': 'Dermatologist specializing in skin cancer detection and cosmetic procedures.'
        },
        {
            'username': 'dr_williams',
            'first_name': 'Michael',
            'last_name': 'Williams',
            'email': 'dr.williams@medicare.com',
            'specialization': 'Pediatrics',
            'license_number': 'MD003',
            'phone': '+1-555-0103',
            'experience_years': 10,
            'consultation_fee': 100.00,
            'bio': 'Pediatrician dedicated to providing comprehensive healthcare for children.'
        },
        {
            'username': 'dr_brown',
            'first_name': 'Emily',
            'last_name': 'Brown',
            'email': 'dr.brown@medicare.com',
            'specialization': 'Orthopedics',
            'license_number': 'MD004',
            'phone': '+1-555-0104',
            'experience_years': 18,
            'consultation_fee': 180.00,
            'bio': 'Orthopedic surgeon with expertise in joint replacement and sports medicine.'
        },
        {
            'username': 'dr_davis',
            'first_name': 'Robert',
            'last_name': 'Davis',
            'email': 'dr.davis@medicare.com',
            'specialization': 'Neurology',
            'license_number': 'MD005',
            'phone': '+1-555-0105',
            'experience_years': 20,
            'consultation_fee': 200.00,
            'bio': 'Neurologist specializing in brain disorders and neurological conditions.'
        },
        {
            'username': 'dr_wilson',
            'first_name': 'Lisa',
            'last_name': 'Wilson',
            'email': 'dr.wilson@medicare.com',
            'specialization': 'General Medicine',
            'license_number': 'MD006',
            'phone': '+1-555-0106',
            'experience_years': 8,
            'consultation_fee': 80.00,
            'bio': 'General practitioner providing primary healthcare services.'
        }
    ]
    
    for doctor_data in doctors_data:
        # Create user
        user, created = User.objects.get_or_create(
            username=doctor_data['username'],
            defaults={
                'first_name': doctor_data['first_name'],
                'last_name': doctor_data['last_name'],
                'email': doctor_data['email'],
                'is_staff': False
            }
        )
        if created:
            user.set_password('doctor123')
            user.save()
            print(f"Created user: {user.username}")
        
        # Create doctor profile
        specialization = Specialization.objects.get(name=doctor_data['specialization'])
        doctor, created = Doctor.objects.get_or_create(
            user=user,
            defaults={
                'specialization': specialization,
                'license_number': doctor_data['license_number'],
                'phone': doctor_data['phone'],
                'experience_years': doctor_data['experience_years'],
                'consultation_fee': doctor_data['consultation_fee'],
                'bio': doctor_data['bio']
            }
        )
        if created:
            print(f"Created doctor: Dr. {doctor.user.first_name} {doctor.user.last_name}")
            
            # Create schedule for the doctor (Monday to Friday, 9 AM to 5 PM)
            weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
            for day in weekdays:
                schedule, created = DoctorSchedule.objects.get_or_create(
                    doctor=doctor,
                    day_of_week=day,
                    defaults={
                        'start_time': time(9, 0),
                        'end_time': time(17, 0)
                    }
                )
                if created:
                    print(f"Created schedule for Dr. {doctor.user.last_name} on {day}")
            
            # Create time slots for the next 7 days
            today = date.today()
            for i in range(7):
                slot_date = today + timedelta(days=i)
                if slot_date.weekday() < 5:  # Monday to Friday
                    # Create hourly slots from 9 AM to 5 PM
                    for hour in range(9, 17):
                        start_time = time(hour, 0)
                        end_time = time(hour + 1, 0)
                        
                        time_slot, created = TimeSlot.objects.get_or_create(
                            doctor=doctor,
                            date=slot_date,
                            start_time=start_time,
                            defaults={'end_time': end_time}
                        )
    
    # Create sample patients
    patients_data = [
        {
            'username': 'patient1',
            'first_name': 'Alice',
            'last_name': 'Cooper',
            'email': 'alice.cooper@email.com',
            'date_of_birth': date(1985, 5, 15),
            'gender': 'F',
            'phone': '+1-555-1001',
            'address': '123 Main St, New York, NY 10001',
            'blood_group': 'A+',
            'emergency_contact': '+1-555-1002',
            'medical_history': 'No significant medical history',
            'allergies': 'Penicillin'
        },
        {
            'username': 'patient2',
            'first_name': 'Bob',
            'last_name': 'Johnson',
            'email': 'bob.johnson@email.com',
            'date_of_birth': date(1978, 12, 3),
            'gender': 'M',
            'phone': '+1-555-1003',
            'address': '456 Oak Ave, Los Angeles, CA 90210',
            'blood_group': 'O-',
            'emergency_contact': '+1-555-1004',
            'medical_history': 'Hypertension, managed with medication',
            'allergies': 'None known'
        },
        {
            'username': 'patient3',
            'first_name': 'Carol',
            'last_name': 'Davis',
            'email': 'carol.davis@email.com',
            'date_of_birth': date(1992, 8, 22),
            'gender': 'F',
            'phone': '+1-555-1005',
            'address': '789 Pine St, Chicago, IL 60601',
            'blood_group': 'B+',
            'emergency_contact': '+1-555-1006',
            'medical_history': 'Asthma since childhood',
            'allergies': 'Dust, pollen'
        }
    ]
    
    for patient_data in patients_data:
        # Create user
        user, created = User.objects.get_or_create(
            username=patient_data['username'],
            defaults={
                'first_name': patient_data['first_name'],
                'last_name': patient_data['last_name'],
                'email': patient_data['email'],
                'is_staff': False
            }
        )
        if created:
            user.set_password('patient123')
            user.save()
            print(f"Created patient user: {user.username}")
        
        # Create patient profile
        patient, created = Patient.objects.get_or_create(
            user=user,
            defaults={
                'date_of_birth': patient_data['date_of_birth'],
                'gender': patient_data['gender'],
                'phone': patient_data['phone'],
                'address': patient_data['address'],
                'blood_group': patient_data['blood_group'],
                'emergency_contact': patient_data['emergency_contact'],
                'medical_history': patient_data['medical_history'],
                'allergies': patient_data['allergies']
            }
        )
        if created:
            print(f"Created patient: {patient.full_name}")
    
    print("\nSample data created successfully!")
    print("\nLogin credentials:")
    print("Admin: username='admin', password='admin'")
    print("Doctors: username='dr_smith', password='doctor123' (and similar for other doctors)")
    print("Patients: username='patient1', password='patient123' (and similar for other patients)")

if __name__ == '__main__':
    create_sample_data()