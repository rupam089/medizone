from django.db import models
from django.contrib.auth.models import User

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # Doctor's full name
    specialization = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)  # Phone number
    image = models.ImageField(upload_to='doctor_images/', blank=True, null=True)  # Profile image

    def save(self, *args, **kwargs):
        self.user.is_staff = True  # Allow login for doctors
        self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name  # Display full name instead of username


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, default='Unknown')
    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    profile_image = models.ImageField(upload_to='patient_images/', blank=True, null=True)

    def __str__(self):
        return self.full_name  # Display full name instead of username


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved')],
        default='Pending'
    )

    def __str__(self):
        return f"{self.patient.full_name} - {self.doctor.name} - {self.date}"



class Service(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='services/')

    def __str__(self):
        return self.title
