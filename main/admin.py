from django.contrib import admin
from .models import Doctor, Patient, Appointment
from .models import Service

admin.site.register(Service)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'contact')
    search_fields = ('name', 'specialization')

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone', 'date_of_birth', 'gender')
    search_fields = ('user__username', 'full_name', 'phone')
    list_filter = ('gender',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'status')
    list_filter = ('status', 'date')
    search_fields = ('patient__user__username', 'doctor__name')
