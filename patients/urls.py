from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('profile/', views.patient_profile, name='patient_profile'),
    path('profile/create/', views.patient_profile_create, name='patient_profile_create'),
    path('register/', views.patient_register, name='patient_register'),
]