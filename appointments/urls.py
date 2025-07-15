from django.urls import path
from . import views

urlpatterns = [
    path('', views.appointment_list, name='appointment_list'),
    path('book/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('<int:appointment_id>/', views.appointment_detail, name='appointment_detail'),
    path('<int:appointment_id>/cancel/', views.cancel_appointment, name='cancel_appointment'),
]