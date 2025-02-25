from django.shortcuts import redirect
from functools import wraps

def patient_required(view_func):
    """Restrict access to only logged-in patients."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if hasattr(request.user, 'patient'):  # Check if user is a patient
            return view_func(request, *args, **kwargs)
        return redirect('home')  # Redirect unauthorized users
    return wrapper

def doctor_required(view_func):
    """Restrict access to only logged-in doctors."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if hasattr(request.user, 'doctor'):  # Check if user is a doctor
            return view_func(request, *args, **kwargs)
        return redirect('home')  # Redirect unauthorized users
    return wrapper
