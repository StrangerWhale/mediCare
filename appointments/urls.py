from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('book/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('my-appointments/', views.my_appointments, name='my_appointments'),
    path('<int:appointment_id>/cancel/', views.cancel_appointment, name='cancel_appointment'),
    path('<int:appointment_id>/reschedule/', views.reschedule_appointment, name='reschedule_appointment'),
    path('available-slots/<int:doctor_id>/<str:date>/', views.get_available_slots, name='get_available_slots'),
]