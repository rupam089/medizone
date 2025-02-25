from django import forms
from django.contrib.auth.models import User
from .models import Appointment, Patient, Service


class PatientRegisterForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, label="Username")
    full_name = forms.CharField(max_length=255, required=True, label="Full Name")
    email = forms.EmailField(required=True, label="Email")
    phone = forms.CharField(max_length=15, required=True, label="Phone Number")
    address = forms.CharField(widget=forms.Textarea, required=False, label="Address")
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False, label="Date of Birth")
    gender = forms.ChoiceField(choices=Patient.GENDER_CHOICES, required=False, label="Gender")
    profile_image = forms.ImageField(required=False, label="Profile Image")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists. Please choose another one.")
        return username

    def save(self, commit=True):
        username = self.cleaned_data['username']
        full_name = self.cleaned_data['full_name']
        email = self.cleaned_data['email']
        phone = self.cleaned_data['phone']
        address = self.cleaned_data.get('address', '')
        date_of_birth = self.cleaned_data.get('date_of_birth')
        gender = self.cleaned_data.get('gender')
        profile_image = self.cleaned_data.get('profile_image')
        password = self.cleaned_data['password']

        # Create the User instance
        user = User.objects.create(username=username, email=email, first_name=full_name)
        user.set_password(password)

        if commit:
            user.save()
            # Create the Patient instance associated with the user
            Patient.objects.create(
                user=user,
                full_name=full_name,
                phone=phone,
                address=address,
                date_of_birth=date_of_birth,
                gender=gender,
                profile_image=profile_image
            )
        return user

    
    
class AppointmentForm(forms.ModelForm):
    date = forms.DateTimeField(
        widget=forms.TextInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )

    class Meta:
        model = Appointment
        fields = ['doctor', 'date']
        widgets = {
            'doctor': forms.Select(attrs={'class': 'form-control'}),
        }



class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description', 'image']
