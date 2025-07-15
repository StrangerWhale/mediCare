from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('register/', views.patient_register, name='patient_register'),
    path('profile/', views.patient_profile, name='patient_profile'),
    path('dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('medical-records/', views.medical_records, name='medical_records'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
]