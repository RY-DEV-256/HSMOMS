from django.shortcuts import render,redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import Patient, Reminder, PrescriptionFeedback, Appointment, MedicalHistory, Prescription
from .forms import BookAppointmentForm, PrescriptionFeedbackForm, ChangePasswordForm


def book_appointment(request):
    patient = Patient.objects.get(admin=request.user)

    if request.method == "POST":
        form = BookAppointmentForm(request.POST)
        if form.is_valid():
            form.save(patient)
            messages.success(request, 'Appointment Booked Successfully!')
            return redirect('appointment_history')  # Redirect to a success page or the desired page after booking
    else:
        form = BookAppointmentForm()

    return render(request, 'hsmoms/patient/book_appointment.html', {'form':form})

@login_required
def appointment_history(request):
    patient = Patient.objects.get(admin=request.user)
    appointments = Appointment.objects.filter(patient_id=patient)
    return render(request, 'hsmoms/patient/appointment_history.html', {'appointments':appointments})

def cancel_appointment(request, pk):
    appointment = get_object_or_404(Appointment, id=pk, patient_id__admin=request.user)
    appointment.status = 'cancelled'
    appointment.save()
    messages.success(request,'Appointment Cancelled Successfully!')
    return redirect('appointment_history')

def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)  # Important for maintaining the user's session
            messages.success(request, 'Your password has been successfully changed.')
            return redirect('patient_dashboard')  
    else:
        form = ChangePasswordForm(user=request.user)
    
    context = {
        'form': form
    }
    return render(request, 'hsmoms/patient/change_password.html', context)

def my_profile(request):
    patient = Patient.objects.get(admin=request.user)
    
    context = {
        'patient': patient
    }
    return render(request, 'hsmoms/patient/my_profile.html', context)

@login_required
def feedback(request, pk):
    prescription = get_object_or_404(Prescription, id=pk)
    patient = get_object_or_404(Patient, admin=request.user)

    if request.method == 'POST':
        form = PrescriptionFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.prescription_id = prescription
            feedback.patient_id = patient
            feedback.save()
            messages.success(request, 'Feedback Sent Successfully, we will get back to you soon!!')
            return redirect('feedback_history')  # Redirect to a success page or any other page
    else:
        form = PrescriptionFeedbackForm()

    context = {
        'form': form,
        'prescription': prescription
    }
    return render(request, 'hsmoms/patient/feedback.html', context)

def feedback_history(request):
    patient = get_object_or_404(Patient, admin=request.user)
    feedbacks = PrescriptionFeedback.objects.filter(patient_id=patient)
    
    context = {
        'feedbacks': feedbacks
    }
    return render(request, 'hsmoms/patient/feedback_history.html', context)
@login_required
def medical_history(request):
    patient = Patient.objects.get(admin=request.user)
    medical_history = MedicalHistory.objects.filter(patient_id=patient)
    context = {
        'medical_history': medical_history
    }
    return render(request, 'hsmoms/patient/medical_history.html', context)

def prescription(request):
    patient = get_object_or_404(Patient, admin=request.user)
    prescriptions = Prescription.objects.filter(medical_history_id__patient_id=patient)
    
    context = {
        'prescriptions': prescriptions
    }
    return render(request, 'hsmoms/patient/prescription.html', context)


def patient_reminder(request):
    patient = get_object_or_404(Patient, admin=request.user)
    reminders = Reminder.objects.filter(patient=patient)
    return render(request, 'hsmoms/patient/reminders.html', {'reminders':reminders})