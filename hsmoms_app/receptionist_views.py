from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Receptionist, Appointment, Reminder, Prescription, PrescriptionFeedback, ContactUs, Patient
from django.contrib import messages
from django.utils import timezone
from .forms import ChangePasswordForm
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def view_appointments(request):
    appointments = Appointment.objects.all()
    context = {
        'appointments': appointments,
    }
    return render(request, 'hsmoms/receptionist/view_appointment.html', context)

def view_patients(request):
    patients = Patient.objects.all()
    # handle search
    search = request.GET.get('q')
    if search:
        patients = patients.filter(first_name__icontains=search)
    p = Paginator(patients, 5)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    context = {
       'page_obj': page_obj,}
    return render(request, 'hsmoms/receptionist/view_patients.html', context)

def view_contact_us(request):
    contact_us_list = ContactUs.objects.all()

    context = {
        'contact_us_list': contact_us_list
    }
    return render(request, 'hsmoms/receptionist/view_contact_us.html', context)

def view_patient_feedback(request):
    feedback = PrescriptionFeedback.objects.all()
    context = {
        'feedback' : feedback,
    }
    return render(request, 'hsmoms/receptionist/view_patient_feedback.html', context)

def monitor_prescriptions(request):
    prescriptions = Prescription.objects.select_related('medical_history_id__doctor_id', 'medical_history_id__patient_id').all()
    return render(request, 'hsmoms/receptionist/prescriptions.html', {'prescriptions': prescriptions})

def my_profile(request):
    receptionist = Receptionist.objects.get(admin=request.user)

    context = {
        'receptionist': receptionist
    }
    return render(request, 'hsmoms/receptionist/my_profile.html', context)

def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)  # Important for maintaining the user's session
            messages.success(request, 'Your password has been successfully changed.')
            return redirect('receptionist_dashboard')  
    else:
        form = ChangePasswordForm(user=request.user)
    
    context = {
        'form': form
    }
    return render(request, 'hsmoms/receptionist/change_password.html', context)


def send_reminder(request, pk):
    patient = get_object_or_404(Patient, id=pk)
    message = "Please don't forget to take your medicine at the right time"
    send_at = timezone.now()  # You can set this to any specific time you need
    reminder = Reminder.objects.create(patient=patient, message=message, send_at=send_at, sent=True)
    messages.success(request, f"Reminder sent to {patient.admin.username}")
    return redirect('list_reminders')

def list_remainders(request):
    reminders = Reminder.objects.all()
    return render(request, 'hsmoms/receptionist/remainder.html',{'reminders': reminders})