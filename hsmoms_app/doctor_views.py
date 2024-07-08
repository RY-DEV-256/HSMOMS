from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .models import Patient, WeeklyReport, PrescriptionFeedback, Appointment, NewPrescription, Doctor, MedicalHistory, Prescription
from .forms import MedicalHistoryForm, ChangePasswordForm, WeeklyReportForm, PrescriptionForm, NewPrescriptionForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
    return render(request, 'hsmoms/doctor/patients.html', context)
def add_medical_records(request, pk):
    patient = get_object_or_404(Patient, id=pk)
    doctor = get_object_or_404(Doctor, admin=request.user)

    if request.method == 'POST':
        form = MedicalHistoryForm(request.POST)
        if form.is_valid():
            medical_history = form.save(commit=False)
            medical_history.patient_id = patient
            medical_history.doctor_id = doctor
            medical_history.save()
            messages.success(request, 'Medical Records Added Successfully!')
            return redirect('doc_view_medical_records')  # Replace with your desired redirect view
    else:
        form = MedicalHistoryForm()

    context = {
        'form': form,
        'patient': patient
    }
    return render(request, 'hsmoms/doctor/add_medical_records.html', context)


def view_prescriptions(request):
    doctor = request.user.doctor 

    prescriptions = Prescription.objects.filter(medical_history_id__doctor_id=doctor)

    context = {
        'prescriptions': prescriptions
    }
    return render(request, 'hsmoms/doctor/prescriptions.html', context)


def view_medical_records(request):
    doctor = Doctor.objects.get(admin=request.user)
    medical_histories = MedicalHistory.objects.filter(doctor_id=doctor)
   

    context = {
        'medical_histories': medical_histories
    }
    return render(request, 'hsmoms/doctor/medical_records.html', context)



@login_required
def add_prescription(request, pk):
    history = get_object_or_404(MedicalHistory, id=pk)
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.medical_history_id = history
            prescription.status = 'on_going'
            prescription.save()

            # Update medical history status
            history.status = 'prescribed'
            history.save()

            messages.success(request, 'Prescriptions Added Successfully!')
            return redirect('doc_view_prescriptions')  # Redirect to the medical history view
    else:
        form = PrescriptionForm()

    context = {
        'form': form,
        'history': history
    }
    return render(request, 'hsmoms/doctor/add_prescription.html', context)

def change_prescription(request, pk):
    pres = get_object_or_404(Prescription, id=pk)
    if request.method == 'POST':
        form = NewPrescriptionForm(request.POST)
        if form.is_valid():
            newprescription = form.save(commit=False)
            newprescription.prescription_id = pres
            newprescription.status = 'on_going'
            newprescription.save()

            # Update prescription status
            pres.status = 'changed'
            pres.save()

            messages.success(request, 'Prescriptions Changed Successfully!')
            return redirect('doc_view_changed_pres')  # Redirect to the medical history view
    else:
        form = NewPrescriptionForm()

    context = {
        'form': form,
        'pres': pres
    }
    return render(request, 'hsmoms/doctor/new_prescription.html', context)

def completed_prescription(request, pk):
    pres = get_object_or_404(Prescription, id=pk)
    pres.status = 'completed'
    pres.save()
    messages.success(request, 'Prescription Status Updated Successfully!')
    return redirect('doc_view_prescriptions')


def completed_newprescription(request, pk):
    pres = get_object_or_404(NewPrescription, id=pk)
    pres.status = 'completed'
    pres.save()
    messages.success(request, 'Prescription Status Updated Successfully!')
    return redirect('doc_view_changed_pres')

@login_required
def view_appointments(request):
    doctor_id = request.user.doctor.id
    appointments = Appointment.objects.filter(doctor_id=doctor_id).order_by('-date', 'time')
    
    context = {
        'appointments': appointments
    }
    return render(request, 'hsmoms/doctor/appointments.html' ,context)

def confirm_appointment(request, pk):
    appointment = get_object_or_404(Appointment, id=pk, doctor_id__admin=request.user)
    appointment.status = 'active'
    appointment.save()
    messages.success(request,'Appointment Confirmed Successfully!')
    return redirect('doc_view_appointments')

def cancel_appointment(request, pk):
    appointment = get_object_or_404(Appointment, id=pk, doctor_id__admin=request.user)
    appointment.status = 'cancelled'
    appointment.save()
    messages.success(request,'Appointment Cancelled Successfully!')
    return redirect('doc_view_appointments')

def view_changed_pres(request):
    doctor = request.user.doctor
    
    # Get MedicalHistory entries for the logged-in doctor
    medical_histories = MedicalHistory.objects.filter(doctor_id=doctor.id)
    
    # Get related prescriptions
    prescriptions = Prescription.objects.filter(medical_history_id__in=medical_histories)
    
    # Get NewPrescriptions related to the above prescriptions
    new_prescriptions = NewPrescription.objects.filter(prescription_id__in=prescriptions)
    
    # Add patient names to the NewPrescription entries
    new_prescriptions_with_patient_info = []
    for new_prescription in new_prescriptions:
        patient = new_prescription.prescription_id.medical_history_id.patient_id
        new_prescriptions_with_patient_info.append({
            'new_prescription': new_prescription,
            'patient_name': f"{patient.admin.first_name} {patient.admin.last_name}",
        })
    
    context = {
        'new_prescriptions_with_patient_info': new_prescriptions_with_patient_info
    }
    return render(request, 'hsmoms/doctor/changed_pres.html', context)

def create_report(request):
    if request.method == 'POST':
        form = WeeklyReportForm(request.POST)
        if form.is_valid():
            weekly_report = form.save(commit=False)
            weekly_report.doctor_id = request.user.doctor  # Assuming you have a way to get the logged-in doctor's instance
            weekly_report.save()
            messages.success(request, 'Report Created Successfully!')
            return redirect('doc_manage_reports')  # Replace 'success_page' with your desired success URL
    else:
        form = WeeklyReportForm()
    return render(request, 'hsmoms/doctor/create_report.html', {'form':form})

@login_required
def manage_reports(request):
    doctor = request.user.doctor  # Assuming you have a way to get the logged-in doctor's instance
    weekly_reports = WeeklyReport.objects.filter(doctor_id=doctor)
    return render(request, 'hsmoms/doctor/manage_reports.html', {'weekly_reports':weekly_reports})


@login_required
def edit_weekly_report(request, pk):
    report = get_object_or_404(WeeklyReport, id=pk, doctor_id=request.user.doctor)

    if request.method == 'POST':
        form = WeeklyReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            messages.success(request, 'Report Updated Successfully!')
            return redirect('doc_manage_reports')  # Redirect to the list of reports after saving
    else:
        form = WeeklyReportForm(instance=report)
    
    return render(request, 'hsmoms/doctor/edit_weekly_report.html', {'form': form, 'report': report})

@login_required
def my_profile(request):
    doctor = Doctor.objects.get(admin=request.user)
    
    context = {
        'doctor': doctor
    }
    return render(request, 'hsmoms/doctor/my_profile.html', context)


def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)  # Important for maintaining the user's session
            messages.success(request, 'Your password has been successfully changed.')
            return redirect('doctor_dashboard')  
    else:
        form = ChangePasswordForm(user=request.user)
    
    context = {
        'form': form
    }
    return render(request, 'hsmoms/doctor/change_password.html', context)

def patient_feedback(request):
    doctor_id = request.user.doctor.id
    
    # Fetching medical histories where the doctor treated the patient
    medical_histories = MedicalHistory.objects.filter(doctor_id=doctor_id)
    
    # Fetching prescriptions related to these medical histories
    prescriptions = Prescription.objects.filter(medical_history_id__in=medical_histories)
    
    # Fetching prescription feedback based on these prescriptions
    prescription_feedback = PrescriptionFeedback.objects.filter(prescription_id__in=prescriptions)
    
    context = {
        'prescription_feedback': prescription_feedback
    }
    return render(request, 'hsmoms/doctor/patient_feedback.html', context)

def viewed_feedback(request, pk):
    feedback = get_object_or_404(PrescriptionFeedback, id=pk)
    feedback.status = 'active'
    feedback.save()
    messages.success(request,'Feedback Status Updated Successfully!')
    return redirect('doc_patient_feedback')