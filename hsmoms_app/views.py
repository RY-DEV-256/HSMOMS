from django.shortcuts import render, redirect, get_object_or_404
from .forms import AdminLoginForm, ContactUsForm, AddPatientForm, CustomLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Appointment, Patient, Reminder, ContactUs, PrescriptionFeedback, Prescription

# Create your views here.
def home(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ' Your message has been sent successfully!, We will contact you shortly.')
            return redirect('home')  
    else:
        form = ContactUsForm()

    context = {
        'form': form
    }
    return render(request, 'hsmoms/home.html', context)

def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = AdminLoginForm()
    return render(request, 'hsmoms/admin_login.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.user_type == 1:
                    return redirect('doctor_dashboard')
                elif user.user_type == 2:
                    return redirect('patient_dashboard')
                elif user.user_type == 3:
                    return redirect('receptionist_dashboard')
                elif user.user_type == 4:
                    return redirect('admin_dashboard')
            else:
                form.add_error(None, "Invalid username or password.")
        else:
            form.add_error(None, "Invalid username or password.")
    else:
        form = CustomLoginForm()
    return render(request, 'hsmoms/login.html', {'form': form})

def patient_register(request):
    if request.method == 'POST':
        form = AddPatientForm(request.POST, request.FILES)
        if form.is_valid():
           form.save()
           messages.success(request, 'Patient Registered Successfully!, Proceed to Login')
           return redirect('login')
    else:
        form = AddPatientForm()
    return render(request, 'hsmoms/patient_register.html', {'form':form})


@login_required
def doctor_dashboard(request):
    doctor_id = request.user.doctor.id
    
    pending_appointments_count = Appointment.objects.filter(doctor_id=doctor_id, status='pending').count()
    
    active_appointments_count = Appointment.objects.filter(doctor_id=doctor_id, status='active').count()
    
    prescriptions = Prescription.objects.filter(medical_history_id__doctor_id=doctor_id)
    
    unviewed_feedback_count = PrescriptionFeedback.objects.filter(prescription_id__in=prescriptions, status='unviewed').count()
    
    context = {
        'pending_appointments_count': pending_appointments_count,
        'active_appointments_count': active_appointments_count,
        'unviewed_feedback_count': unviewed_feedback_count
    }
    return render(request, 'hsmoms/doctor/doctor_dashboard.html', context)

@login_required
def patient_dashboard(request):
    patient = get_object_or_404(Patient, admin=request.user)
    reminders = Reminder.objects.filter(patient=patient).count()
    return render(request, 'hsmoms/patient/patient_dashboard.html', {'reminders':reminders})

@login_required
def receptionist_dashboard(request):
    pending_appointments_count = Appointment.objects.filter(status='pending').count()

    # Count ongoing prescriptions
    ongoing_prescriptions_count = Prescription.objects.filter(status='on_going').count()

    # Count contact us queries
    contact_us_queries_count = ContactUs.objects.all().count()

    context = {
        'pending_appointments_count': pending_appointments_count,
        'ongoing_prescriptions_count': ongoing_prescriptions_count,
        'contact_us_queries_count': contact_us_queries_count,
    }
    return render(request, 'hsmoms/receptionist/receptionist_dashboard.html', context)

def admin_logout(request):
    logout(request)
    return redirect('admin_login')

def logout_view(request):
    logout(request)
    return redirect('login')