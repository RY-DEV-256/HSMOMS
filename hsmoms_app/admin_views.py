from django.shortcuts import render,redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from .forms import SpecializationForm, EditPatientForm, EditReceptionistForm, AddReceptionistForm, ScheduleForm, AddDoctorForm, EditDoctorForm
from .models import Specialization, PrescriptionFeedback, Appointment, CustomUser, PrescriptionFeedback, Appointment , Prescription, WeeklyReport, Schedule, Doctor, Receptionist, Patient
from django.core.files.storage import FileSystemStorage
# from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def admin_dashboard(request):
    patients_count = CustomUser.objects.filter(user_type=2).count()
    doctors_count = CustomUser.objects.filter(user_type=1).count()
    receptionists_count = CustomUser.objects.filter(user_type=3).count()
    users_count = CustomUser.objects.count()
    appointments_count = Appointment.objects.filter(status='pending').count()
    prescription_feedback_count = PrescriptionFeedback.objects.filter(status='unviewed').count()
    context = {
        'patients_count': patients_count,
        'doctors_count': doctors_count,
        'users_count': users_count,
        'receptionists_count': receptionists_count,
        'appointments_count': appointments_count,
        'prescription_feedback_count': prescription_feedback_count,
    }
    return render(request, 'hsmoms/admin/admin_dashboard.html', context)
# ========================Receptionist=======================================
def manage_receptionists(request):
    receptionists = Receptionist.objects.all()
    # handle search
    search = request.GET.get('q')
    if search:
        receptionists = receptionists.filter(first_name__icontains=search)
    p = Paginator(receptionists, 5)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    context = {
       'page_obj': page_obj,}
    return render(request, 'hsmoms/admin/manage_receptionists.html', context)

def create_receptionist(request):
    if request.method == 'POST':
        form = AddReceptionistForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Receptionist added successfully.')
            return redirect('manage_receptionists')
        else:
            messages.warning(request, 'Please correct the error below.')
    else:
        form = AddReceptionistForm()
    return render(request, 'hsmoms/admin/create_receptionist.html', {'form':form})

def edit_receptionist(request, pk):
    user_instance = get_object_or_404(CustomUser, id=pk)
    receptionist_instance = get_object_or_404(Receptionist, admin=user_instance)

    if request.method == 'POST':
        form = EditReceptionistForm(request.POST, request.FILES, 
                                    user_instance=user_instance, 
                                    receptionist_instance=receptionist_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Receptionist updated successfully.')
            return redirect('manage_receptionists')
        else:
            messages.warning(request, 'Please correct the error below.')
    else:
        initial_data = {
            'email': user_instance.email,
            'first_name': user_instance.first_name,
            'last_name': user_instance.last_name,
            'username': user_instance.username,
            'address': receptionist_instance.address,
            'phone': receptionist_instance.phone,
            'profile_pic': receptionist_instance.profile_pic,
        }
        form = EditReceptionistForm(initial=initial_data, 
                                    user_instance=user_instance, 
                                    receptionist_instance=receptionist_instance)
    return render(request, 'hsmoms/admin/edit_receptionist.html', {'form':form})

def delete_receptionist(request, pk):
    receptionist = CustomUser.objects.get(id=pk)
    receptionist.delete()
    messages.success(request, 'Receptionist Deleted Successfully!')
    return redirect('manage_receptionists')

# ========================Specialization=======================================
def manage_specialization(request):
    if request.method == 'POST':
        form = SpecializationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Specialization Added Successfully!")
            return redirect('manage_specialization')  # Redirect to the list of specializations after adding
    else:
        form = SpecializationForm()
        specialization = Specialization.objects.all()
        search = request.GET.get('q')
        if search:
            specialization = specialization.filter(field__icontains=search)
        p = Paginator(specialization, 8)
        page_number = request.GET.get('page')
        try:
            page_obj = p.get_page(page_number)
        except PageNotAnInteger:
            page_obj = p.page(1)
        except EmptyPage:
            page_obj = p.page(p.num_pages)
        context = {
            'form': form,
        'page_obj': page_obj,}
    return render(request, 'hsmoms/admin/manage_specialization.html', context)

def edit_specialization(request, pk):
    specialization = get_object_or_404(Specialization, pk=pk)
    if request.method == 'POST':
        form = SpecializationForm(request.POST, instance=specialization)
        if form.is_valid():
            form.save()
            messages.success(request, 'Specialization Updated Successfully!')
            return redirect('manage_specialization')  # Redirect to the list of specializations after editing
    else:
        form = SpecializationForm(instance=specialization)
    return render(request, 'hsmoms/admin/edit_specialization.html', {'form': form})

def delete_specialization(request, pk):
    spec = Specialization.objects.get(id=pk)
    spec.delete()
    messages.success(request, 'Specialization Deleted Successfully!')
    return redirect('manage_specialization')

# ========================Schedule=======================================
def manage_schedule(request):
    schedules = Schedule.objects.all()
    context = {
       'schedules': schedules,}
    return render(request, 'hsmoms/admin/manage_schedule.html', context)

def add_schedule(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Schedule Added Successfully!")
            return redirect('manage_schedule')  # Redirect to the list of schedules after adding
    else:
        form = ScheduleForm()
    return render(request, 'hsmoms/admin/add_schedule.html', {'form': form})

def edit_schedule(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    if request.method == 'POST':
        form = ScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            messages.success(request, 'Schedule Updated Successfully!')
            return redirect('manage_schedule')  
    else:
        form = ScheduleForm(instance=schedule)
    return render(request, 'hsmoms/admin/edit_schedule.html', {'form': form})

def delete_schedule(request, pk):
    schedule = Schedule.objects.get(id=pk)
    schedule.delete()
    messages.success(request, 'Schedule Deleted Successfully!')
    return redirect('manage_schedule')


# ========================Doctor=======================================
def manage_doctors(request):
    doctors = Doctor.objects.all()
    # handle search
    search = request.GET.get('q')
    if search:
        doctors = doctors.filter(first_name__icontains=search)
    p = Paginator(doctors, 5)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    context = {
       'page_obj': page_obj,
    }
    return render(request, 'hsmoms/admin/manage_doctors.html', context)

def create_doctor(request):
    if request.method == 'POST':
        form = AddDoctorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor added successfully.')
            return redirect('manage_doctors')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = AddDoctorForm()
    return render(request, 'hsmoms/admin/create_doctor.html', {'form': form})

def edit_doctor(request, pk):
    user_instance = get_object_or_404(CustomUser, id=pk, user_type=1)
    doctor_instance = get_object_or_404(Doctor, admin=user_instance)
    
    if request.method == 'POST':
        form = EditDoctorForm(request.POST, request.FILES, user_instance=user_instance, doctor_instance=doctor_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor updated successfully.')
            return redirect('manage_doctors')
        else:
            messages.warning(request, 'Please correct the error below.')
    else:
        form = EditDoctorForm(user_instance=user_instance, doctor_instance=doctor_instance)
    
    return render(request, 'hsmoms/admin/edit_doctor.html', {'form': form})

def delete_doctor(request, pk):
    doctor = CustomUser.objects.get(id=pk)
    doctor.delete()
    messages.success(request, 'Doctor Deleted Successfully!')
    return redirect('manage_doctors')



def manage_patients(request):
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
    return render(request, 'hsmoms/admin/manage_patients.html', context)

def edit_patient(request, pk):
    user_instance = get_object_or_404(CustomUser, id=pk)
    patient_instance = get_object_or_404(Patient, admin=user_instance)

    if request.method == 'POST':
        form = EditPatientForm(request.POST, request.FILES, 
                               user_instance=user_instance, 
                               patient_instance=patient_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient updated successfully.')
            return redirect('manage_patients')
        else:
            messages.warning(request, 'Please correct the error below.')
    else:
        initial_data = {
            'email': user_instance.email,
            'first_name': user_instance.first_name,
            'last_name': user_instance.last_name,
            'username': user_instance.username,
            'address': patient_instance.address,
            'age': patient_instance.age,
            'phone': patient_instance.phone,
            'gender': patient_instance.gender,
            'profile_pic': patient_instance.profile_pic,
        }
        form = EditPatientForm(initial=initial_data, 
                               user_instance=user_instance, 
                               patient_instance=patient_instance)
    
    return render(request, 'hsmoms/admin/edit_patient.html', {'form': form})

def delete_patient(request, pk):
    patient = CustomUser.objects.get(id=pk)
    patient.delete()
    messages.success(request, 'Patient Deleted Successfully!')
    return redirect('manage_patients')



def view_appointments(request):
    appointments = Appointment.objects.all()
    context = {
        'appointments': appointments,
    }
    return render(request, 'hsmoms/admin/view_appointments.html', context)

def view_prescriptions(request):
    prescriptions = Prescription.objects.select_related('medical_history_id__doctor_id', 'medical_history_id__patient_id').all()
    
    context = {
        'prescriptions': prescriptions
    }
    return render(request, 'hsmoms/admin/view_prescriptions.html', context)

def view_reports(request):
    reports = WeeklyReport.objects.all()
    context = {
        'reports' : reports,
    }
    return render(request, 'hsmoms/admin/view_reports.html', context)

def feedback_on_prescriptions(request):
    feedback = PrescriptionFeedback.objects.all()
    context = {
        'feedback' : feedback,
    }
    return render(request, 'hsmoms/admin/feedback_on_prescriptions.html', context)

