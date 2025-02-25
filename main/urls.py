from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    
    # Patient Authentication & Dashboard
    path('register/', views.register_patient, name='register'),
    path('login/', LoginView.as_view(template_name='patient_login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),

    # Doctor Authentication & Dashboard
    path('doctor_login/', LoginView.as_view(template_name='doctor_login.html', next_page='doctor_dashboard'), name='doctor_login'),
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    
    # Appointments
    path('book/', views.book_appointment, name='book_appointment'),
    path('approve_appointment/<int:appointment_id>/', views.approve_appointment, name='approve_appointment'),
    path('reject_appointment/<int:appointment_id>/', views.reject_appointment, name='reject_appointment'),
    path('appointment_info/', views.appointment_info, name='appointment_info'),

    # Services
    path('services/', views.service_list, name='service_list'),
    path('services/add/', views.add_service, name='add_service'),

    # Profile (For future user profile picture handling)
    path('profile/', views.profile_view, name='profile'),

    path('contact/', views.contact_view, name='contact'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
