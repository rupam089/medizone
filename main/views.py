from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import PatientRegisterForm, AppointmentForm, ServiceForm
from .models import Doctor, Appointment, Patient, Service
from django.contrib.admin.views.decorators import staff_member_required
from .decorators import patient_required, doctor_required


def home(request):
    """Homepage displaying available doctors."""
    doctors = Doctor.objects.all()
    return render(request, 'home.html', {'doctors': doctors})


def appointment_info(request):
    """Show appointment info or redirect logged-in users."""
    if request.user.is_authenticated:
        return redirect('book_appointment')

    doctors = Doctor.objects.all()
    return render(request, 'appointment_info.html', {'doctors': doctors})


def register_patient(request):
    """Handles patient registration."""
    if request.method == 'POST':
        form = PatientRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')
    else:
        form = PatientRegisterForm()
    
    return render(request, 'patient_register.html', {'form': form})


@login_required
@patient_required
def book_appointment(request):
    """Allows patients to book an appointment."""
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient
            appointment.status = "Pending"
            appointment.save()
            messages.success(request, "Appointment booked successfully! Waiting for doctor's approval.")
            return redirect('patient_dashboard')
    else:
        form = AppointmentForm()
    
    return render(request, 'book_appointment.html', {'form': form})


@login_required
@doctor_required
def doctor_dashboard(request):
    """Doctor dashboard to view pending & approved appointments."""
    doctor = request.user.doctor
    pending_appointments = Appointment.objects.filter(doctor=doctor, status="Pending")
    approved_appointments = Appointment.objects.filter(doctor=doctor, status="Approved")
    password_form = PasswordChangeForm(request.user)

    return render(request, 'doctor_dashboard.html', {
        'doctor': doctor,
        'pending_appointments': pending_appointments,
        'approved_appointments': approved_appointments,
        'password_form': password_form
    })


@login_required
@doctor_required
def approve_appointment(request, appointment_id):
    """Allows doctors to approve appointments."""
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user.doctor)

    if request.method == "POST":
        appointment.status = "Approved"
        appointment.save()
        messages.success(request, "Appointment approved successfully.")

    return redirect('doctor_dashboard')


@login_required
@doctor_required
def reject_appointment(request, appointment_id):
    """Allows doctors to reject & delete appointments."""
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user.doctor)

    if request.method == "POST":
        appointment.delete()
        messages.success(request, "Appointment rejected successfully.")

    return redirect('doctor_dashboard')


def patient_login(request):
    """Handles patient and doctor login."""
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Redirect based on user type
            if hasattr(user, 'patient'):
                return redirect('patient_dashboard')
            elif hasattr(user, 'doctor'):
                return redirect('doctor_dashboard')
            else:
                return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, "patient_login.html", {"form": form})


@login_required
@patient_required
def patient_dashboard(request):
    """Patient dashboard to manage appointments."""
    patient = request.user.patient
    appointments = Appointment.objects.filter(patient=patient).select_related('doctor').order_by('-date')
    password_form = PasswordChangeForm(request.user)

    return render(request, 'patient_dashboard.html', {
        'patient': patient,
        'appointments': appointments,
        'password_form': password_form
    })


@login_required
def logout_view(request):
    """Logs out the user and redirects to home."""
    if request.method == "POST":
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect('home')
    
    messages.error(request, "Invalid request method.")
    return redirect('home')


# @login_required
# @doctor_required
def service_list(request):
    """Displays all available services (only for doctors)."""
    services = Service.objects.all()
    return render(request, 'services.html', {'services': services})


@staff_member_required
def add_service(request):
    """Allows admin to add new services."""
    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Service added successfully.")
            return redirect('service_list')
    else:
        form = ServiceForm()
    
    return render(request, 'add_service.html', {'form': form})

@login_required
def profile_view(request):
    """Displays user profile (Patient or Doctor)"""
    user = request.user
    context = {'user': user}
    return render(request, 'profile.html', context)


from django.shortcuts import render, redirect
from django.contrib import messages

def contact_view(request):
    """Display and process the Contact Us form."""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # TODO: Save to DB, send email, etc.
        messages.success(request, "Thank you for contacting us! We’ll get back to you soon.")
        return redirect('contact')  # Redirect to same page to clear form

    return render(request, 'contact.html')
