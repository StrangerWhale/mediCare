from django.urls import path
from . import views

app_name = 'doctors'

urlpatterns = [
    path('', views.doctor_list, name='doctor_list'),
    path('<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
    path('register/', views.doctor_register, name='doctor_register'),
    path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('schedule/', views.manage_schedule, name='manage_schedule'),
    path('appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('appointment/<int:appointment_id>/update/', views.update_appointment, name='update_appointment'),
]