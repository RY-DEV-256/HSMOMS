from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'Doctor'),
        (2, 'Patient'),
        (3, 'Receptionist'),
        (4, 'Admin'),
    )
    id = models.AutoField(primary_key=True)
    user_type = models.IntegerField(choices=USER_TYPE_CHOICES, default=1)

class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    gender = models.CharField(max_length=30)
    age = models.CharField(max_length=20)
    first_name = models.CharField(max_length=30, default='ry')
    phone = models.TextField(max_length=30)
    address = models.TextField(max_length=30)
    profile_pic = models.ImageField(null=True, blank=False, upload_to="profile_images/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    phone = models.TextField(max_length=30)
    address = models.TextField(max_length=30)
    profile_pic = models.ImageField(null=True, blank=False, upload_to="profile_images/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Receptionist(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    email = models.EmailField(unique=True)
    phone = models.TextField(max_length=30)
    first_name = models.CharField(max_length=30, default='ry')
    address = models.TextField(max_length=30)
    profile_pic = models.ImageField(null=True, blank=False, upload_to="profile_images/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
class Specialization(models.Model):
    id = models.AutoField(primary_key=True)
    field = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Schedule(models.Model):
    id = models.AutoField(primary_key=True)
    working_days = models.TextField()
    working_time = models.TextField()
    objects = models.Manager()

class Doctor(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    phone = models.TextField()
    first_name = models.CharField(max_length=30, default='ry')
    address = models.TextField()
    profile_pic = models.ImageField(null=True, blank=False, upload_to="profile_images/")
    specialization_id = models.ForeignKey(Specialization, on_delete=models.DO_NOTHING)
    schedule_id = models.ForeignKey(Schedule, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
   
class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.CharField(max_length=50)
    consultancy_fee = models.CharField(max_length=30, default="10000")
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class MedicalHistory(models.Model):
    id = models.AutoField(primary_key=True)
    blood_sugar = models.CharField(max_length=20)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE, default=1)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE, default=1)
    illnes = models.CharField(max_length=20, default='fever')
    blood_pressure = models.CharField(max_length=20)
    weight = models.CharField(max_length=20)
    height = models.CharField(max_length=20)
    body_temp = models.CharField(max_length=20)
    visit_date = models.DateField()
    status = models.CharField(max_length=30, default='unprescribed')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    
class Prescription(models.Model):
    id = models.AutoField(primary_key=True)
    medical_history_id = models.ForeignKey(MedicalHistory, on_delete=models.CASCADE, default=1)
    medication = models.TextField()
    dosage = models.TextField()
    instructions = models.TextField()
    status = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class NewPrescription(models.Model):
    id = models.AutoField(primary_key=True)
    prescription_id = models.ForeignKey(Prescription, on_delete=models.CASCADE , default='1')
    medication = models.TextField()
    dosage = models.TextField()
    instructions = models.TextField()
    reason = models.TextField()
    status = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class PrescriptionFeedback(models.Model):
    id = models.AutoField(primary_key=True)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE, default=1)
    prescription_id = models.ForeignKey(Prescription, on_delete=models.CASCADE, default=1)
    outcome = models.TextField()
    recommendations = models.TextField()
    status = models.CharField(max_length=30, default='unviewed')
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class WeeklyReport(models.Model):
    id = models.AutoField(primary_key=True)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    overview = models.TextField()
    outcomes = models.TextField()
    duration = models.TextField()
    challenges = models.TextField()
    recommendations = models.TextField()
    conclusion = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Reminder(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    message = models.TextField()
    send_at = models.DateTimeField()
    sent = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default='pending')
    objects = models.Manager()


class ContactUs(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()




