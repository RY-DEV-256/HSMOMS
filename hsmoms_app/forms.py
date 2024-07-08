from django import forms
from .models import CustomUser, ContactUs, PrescriptionFeedback, Appointment, WeeklyReport, NewPrescription, Prescription, MedicalHistory, Receptionist, Patient, Schedule, Specialization, Doctor
from django.contrib.auth.forms import AuthenticationForm
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate
# from django.core.exceptions import ValidationError

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class AdminLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class AddPatientForm(forms.Form):
    email = forms.EmailField(label="Email",
                             max_length=50,
                             widget=forms.EmailInput(attrs={"class":"form-control"}))
    
    first_name = forms.CharField(label="First Name",
                                 max_length=50,
                                 widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name",
                                max_length=50,
                                widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username",
                               max_length=50,
                               widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address",
                              max_length=50,
                              widget=forms.TextInput(attrs={"class":"form-control"}))
    age = forms.CharField(label="Age",
                              max_length=50,
                              widget=forms.TextInput(attrs={"class":"form-control"}))
     
    phone = forms.CharField(label="Phone Number",
                              max_length=50,
                              widget=forms.TextInput(attrs={"class":"form-control"}))
     
    gender_list = (
        (None, "Select"),
        ('Male','Male'),
        ('Female','Female')
    )
     
    
    gender = forms.ChoiceField(label="Gender",
                               choices=gender_list,
                               widget=forms.Select(attrs={"class":"form-control"}))
  
    profile_pic = forms.FileField(label="Profile Pic",
                                  required=False,
                                  widget=forms.FileInput(attrs={"class":"form-control"}))
    password1 = forms.CharField(label="Password",
                               max_length=50,
                               widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            self.add_error('username', "Username already exists")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            self.add_error('email', "Username already exists")
        return email
    

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match")
        return password2
    
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if not age.isdigit():
            self.add_error('age', "Age must be a number")
        return age
    
    def save(self, commit=True):
        user = CustomUser(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            user_type=2
        )
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()

            profile_pic_url = None
            if 'profile_pic' in self.files:
                profile_pic = self.files['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)

            patient = Patient(
                admin=user,
                first_name=self.cleaned_data['first_name'],
                gender=self.cleaned_data['gender'],
                age=self.cleaned_data['age'],
                phone=self.cleaned_data['phone'],
                address=self.cleaned_data['address'],
                profile_pic=profile_pic_url
            )
            patient.save()
        return user
    
class EditPatientForm(forms.Form):
    email = forms.EmailField(label="Email",
                             max_length=50,
                             widget=forms.EmailInput(attrs={"class":"form-control"}))
    
    first_name = forms.CharField(label="First Name",
                                 max_length=50,
                                 widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name",
                                max_length=50,
                                widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username",
                               max_length=50,
                               widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address",
                              max_length=50,
                              widget=forms.TextInput(attrs={"class":"form-control"}))
    age = forms.CharField(label="Age",
                          max_length=50,
                          widget=forms.TextInput(attrs={"class":"form-control"}))
    
    phone = forms.CharField(label="Phone Number",
                            max_length=50,
                            widget=forms.TextInput(attrs={"class":"form-control"}))
    
    gender_list = (
        (None, "Select"),
        ('Male','Male'),
        ('Female','Female')
    )
    
    gender = forms.ChoiceField(label="Gender",
                               choices=gender_list,
                               widget=forms.Select(attrs={"class":"form-control"}))
    
    profile_pic = forms.FileField(label="Profile Pic",
                                  required=False,
                                  widget=forms.FileInput(attrs={"class":"form-control"}))
    
    password1 = forms.CharField(label="Password",
                                max_length=50,
                                widget=forms.PasswordInput(attrs={"class":"form-control"}),
                                required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}),
                                label='Confirm Password',
                                required=False)
    
    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.pop('user_instance', None)
        self.patient_instance = kwargs.pop('patient_instance', None)
        super(EditPatientForm, self).__init__(*args, **kwargs)
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exclude(id=self.user_instance.id).exists():
            self.add_error('username', "Username already exists")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exclude(id=self.user_instance.id).exists():
            self.add_error('email', "Email already exists")
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match")
        return password2
    
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if not age.isdigit():
            self.add_error('age', "Age must be a number")
        return age
    
    def save(self, commit=True):
        user = self.user_instance
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if self.cleaned_data['password1']:
            user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            
            profile_pic_url = self.patient_instance.profile_pic
            if 'profile_pic' in self.files:
                profile_pic = self.files['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            
            patient = self.patient_instance
            patient.gender = self.cleaned_data['gender']
            patient.age = self.cleaned_data['age']
            patient.first_name = self.cleaned_data['first_name']
            patient.phone = self.cleaned_data['phone']
            patient.address = self.cleaned_data['address']
            patient.profile_pic = profile_pic_url
            if commit:
                patient.save()
        return user
    
class SpecializationForm(forms.ModelForm):
    field = forms.CharField(label="Spec. Name", max_length=50)
    class Meta:
        model = Specialization
        fields = ['field']

    def clean_field(self):
        field = self.cleaned_data.get('field')
        if Specialization.objects.filter(field=field).exists():
            self.add_error("field", 'Specialization already exists.')
        return field
    
class ScheduleForm(forms.ModelForm):
    working_days = forms.CharField(max_length=100)
    working_time = forms.CharField(max_length=100)
    class Meta:
        model = Schedule
        fields = ['working_days', 'working_time']

    def clean(self):
        cleaned_data = super().clean()
        working_days = cleaned_data.get('working_days')
        working_time = cleaned_data.get('working_time')

        if Schedule.objects.filter(working_days=working_days, working_time=working_time).exists():
            raise forms.ValidationError('A schedule with this working days and working time already exists.')

        return cleaned_data
    

class AddDoctorForm(forms.Form):   
    first_name = forms.CharField(label="First Name",
                                 max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name",
                                max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username",
                               max_length=50,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label="Email",
                             max_length=50,
                             widget=forms.EmailInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Address",
                              max_length=50,
                              widget=forms.TextInput(attrs={"class": "form-control"}))
    phone = forms.CharField(label="Phone Number",
                            max_length=50,
                            widget=forms.TextInput(attrs={"class": "form-control"}))
    
    
    try:
        specializations = Specialization.objects.all()
        specialization_list = []
        for spec in specializations:
            single_spec = (spec.id, spec.field) 
            specialization_list.append(single_spec)
    except:
        specialization_list = []

    try:
        schedules = Schedule.objects.all()
        schedule_list = []
        for sch in schedules:
            single_sch = (sch.id, str(sch.working_days)+ " - " +str(sch.working_time))
            schedule_list.append(single_sch)
    except:
        schedule_list = []

    specialization_id = forms.ChoiceField(label="Specialization", choices=specialization_list, widget=forms.Select(attrs={"class": "form-control"}))
    schedule_id = forms.ChoiceField(label="Schedule", choices=schedule_list, widget=forms.Select(attrs={"class": "form-control"}))
    
    profile_pic = forms.FileField(label="Profile Pic",
                                  required=False,
                                  widget=forms.FileInput(attrs={"class": "form-control"}))
  
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            self.add_error('username', "Username already exists")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            self.add_error('email', "Email already exists")
        return email
    
    
    
    def save(self, commit=True):
        user = CustomUser(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            user_type=1  # Doctor user type
        )
        user.set_password("hsmoms@256")
        if commit:
            user.save()
            profile_pic_url = None
            if 'profile_pic' in self.files:
                profile_pic = self.files['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            specialization = Specialization.objects.get(id=self.cleaned_data['specialization_id'])
            schedule = Schedule.objects.get(id=self.cleaned_data['schedule_id'])
            doctor = Doctor(
                admin=user,
                phone=self.cleaned_data['phone'],
                address=self.cleaned_data['address'],
                first_name=self.cleaned_data['first_name'],
                profile_pic=profile_pic_url,
                specialization_id=specialization,
                schedule_id=schedule
            )
            doctor.save()
        return user
    

class EditDoctorForm(forms.Form):
    email = forms.EmailField(label="Email",
                             max_length=50,
                             widget=forms.EmailInput(attrs={"class": "form-control"}))
    
    first_name = forms.CharField(label="First Name",
                                 max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name",
                                max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username",
                               max_length=50,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Address",
                              max_length=50,
                              widget=forms.TextInput(attrs={"class": "form-control"}))
    phone = forms.CharField(label="Phone Number",
                            max_length=50,
                            widget=forms.TextInput(attrs={"class": "form-control"}))
    
    profile_pic = forms.FileField(label="Profile Pic",
                                  required=False,
                                  widget=forms.FileInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(label="Password",
                                max_length=50,
                                widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    
    specialization_id = forms.ChoiceField(label="Specialization", widget=forms.Select(attrs={"class": "form-control"}))
    schedule_id = forms.ChoiceField(label="Schedule", widget=forms.Select(attrs={"class": "form-control"}))
    
    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.pop('user_instance', None)
        self.doctor_instance = kwargs.pop('doctor_instance', None)
        super(EditDoctorForm, self).__init__(*args, **kwargs)
        
        specializations = Specialization.objects.all()
        specialization_list = [(spec.id, spec.field) for spec in specializations]
        self.fields['specialization_id'].choices = specialization_list

        schedules = Schedule.objects.all()
        schedule_list = [(sch.id, f"{sch.working_days} - {sch.working_time}") for sch in schedules]
        self.fields['schedule_id'].choices = schedule_list

        if self.user_instance:
            self.fields['email'].initial = self.user_instance.email
            self.fields['first_name'].initial = self.user_instance.first_name
            self.fields['last_name'].initial = self.user_instance.last_name
            self.fields['username'].initial = self.user_instance.username
            self.fields['address'].initial = self.doctor_instance.address
            self.fields['phone'].initial = self.doctor_instance.phone
            self.fields['specialization_id'].initial = self.doctor_instance.specialization_id.id
            self.fields['schedule_id'].initial = self.doctor_instance.schedule_id.id
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exclude(pk=self.user_instance.pk).exists():
            self.add_error('username', "Username already exists")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exclude(pk=self.user_instance.pk).exists():
            self.add_error('email', "Email already exists")
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match")
        return password2
    
    def save(self, commit=True):
        if self.user_instance:
            user = self.user_instance
            doctor = self.doctor_instance
        else:
            user = CustomUser(user_type=1)  # Doctor user type
            doctor = Doctor()
            
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if self.cleaned_data['password1']:
            user.set_password(self.cleaned_data['password1'])
        
        if commit:
            user.save()
            
            doctor.admin = user
            doctor.phone = self.cleaned_data['phone']
            doctor.address = self.cleaned_data['address']
            doctor.first_name = self.cleaned_data['first_name']

            profile_pic_url = self.doctor_instance.profile_pic
            if 'profile_pic' in self.files:
                profile_pic = self.files['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)

            doctor.profile_pic = profile_pic_url
            doctor.specialization_id = Specialization.objects.get(id=self.cleaned_data['specialization_id'])
            doctor.schedule_id = Schedule.objects.get(id=self.cleaned_data['schedule_id'])
            doctor.save()
        
        return user 

class AddReceptionistForm(forms.Form):
    email = forms.EmailField(label="Email",
                             max_length=50,
                             widget=forms.EmailInput(attrs={"class": "form-control"}))
    
    first_name = forms.CharField(label="First Name",
                                 max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name",
                                max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username",
                               max_length=50,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Address",
                              max_length=50,
                              widget=forms.TextInput(attrs={"class": "form-control"}))
    phone = forms.CharField(label="Phone Number",
                            max_length=50,
                            widget=forms.TextInput(attrs={"class": "form-control"}))
    
    profile_pic = forms.FileField(label="Profile Pic",
                                  required=False,
                                  widget=forms.FileInput(attrs={"class": "form-control"}))
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            self.add_error('username', "Username already exists")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            self.add_error('email', "Email already exists")
        return email
    
    def save(self, commit=True):
        user = CustomUser(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            user_type=3  # Receptionist user type
        )
        user.set_password("hsmoms@256")
        if commit:
            user.save()
            
            profile_pic_url = None
            if 'profile_pic' in self.files:
                profile_pic = self.files['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            
            receptionist = Receptionist(
                admin=user,
                email=self.cleaned_data['email'],
                phone=self.cleaned_data['phone'],
                first_name=self.cleaned_data['first_name'],
                address=self.cleaned_data['address'],
                profile_pic=profile_pic_url
            )
            receptionist.save()
        return user
    
class EditReceptionistForm(forms.Form):
    email = forms.EmailField(label="Email",
                             max_length=50,
                             widget=forms.EmailInput(attrs={"class": "form-control"}))
    
    first_name = forms.CharField(label="First Name",
                                 max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name",
                                max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username",
                               max_length=50,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Address",
                              max_length=50,
                              widget=forms.TextInput(attrs={"class": "form-control"}))
    phone = forms.CharField(label="Phone Number",
                            max_length=50,
                            widget=forms.TextInput(attrs={"class": "form-control"}))
    
    profile_pic = forms.FileField(label="Profile Pic",
                                  required=False,
                                  widget=forms.FileInput(attrs={"class": "form-control"}))
    
    password1 = forms.CharField(label="Password",
                                max_length=50,
                                widget=forms.PasswordInput(attrs={"class": "form-control"}),
                                required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}), 
                                label='Confirm Password', 
                                required=False)
    
    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.pop('user_instance', None)
        self.receptionist_instance = kwargs.pop('receptionist_instance', None)
        super(EditReceptionistForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exclude(id=self.user_instance.id).exists():
            self.add_error('username', "Username already exists")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exclude(id=self.user_instance.id).exists():
            self.add_error('email', "Email already exists")
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match")
        return password2
    
    def save(self, commit=True):
        user = self.user_instance
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if self.cleaned_data['password1']:
            user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            
            profile_pic_url = self.receptionist_instance.profile_pic
            if 'profile_pic' in self.files:
                profile_pic = self.files['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            
            receptionist = self.receptionist_instance
            receptionist.phone = self.cleaned_data['phone']
            receptionist.address = self.cleaned_data['address']
            receptionist.first_name = self.cleaned_data['first_name']
            receptionist.profile_pic = profile_pic_url
            if commit:
                receptionist.save()
        return user
    

class BookAppointmentForm(forms.Form):
    
    try:
        doctors = Doctor.objects.all()
        doctor_list = []
        for doc in doctors:
            single_doc = (doc.id, str(doc.first_name)+" "+str(doc.admin.last_name)+" "+str(doc.specialization_id.field)) 
            doctor_list.append(single_doc)
    except:
        doctor_list = []
    doctor_id = forms.ChoiceField(label="Doctor with Specialization", choices=doctor_list, widget=forms.Select(attrs={"class": "form-control"}))
    
    date = forms.DateField(
        label="Appointment Date",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })

    )
    time_list = ( 
        (None, 'Select'),
        ('08:00','08:00 AM'), 
        ('10:00','10:00 AM'), 
        ('12:00', '12:00 AM')
    ) 

    time = forms.ChoiceField(label="Appointment Time", choices=time_list, widget=forms.Select(attrs={"class":"form-control"})) 
    
    consultancy_fee = forms.CharField(
        label="Consultancy Fee",
        initial="1000",
        disabled=True,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    def save(self, patient):
        doctor = self.cleaned_data['doctor_id']
        date = self.cleaned_data['date']
        time = self.cleaned_data['time']
        consultancy_fee = self.cleaned_data['consultancy_fee']

        doctor_id = Doctor.objects.get(id=doctor)

        appointment = Appointment(
            patient_id=patient,
            doctor_id=doctor_id,
            date=date,
            time=time,
            consultancy_fee=consultancy_fee,
            status="pending"
        )
        appointment.save()
        return appointment
    

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(label='Current Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not self.user or not authenticate(username=self.user.username, password=current_password):
            self.add_error('current_password', 'Incorrect current password.')
        return current_password

    def clean_confirm_password(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if new_password and confirm_password and new_password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')
        return confirm_password
    


class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        fields = [
            'blood_sugar', 
            'illnes', 
            'blood_pressure', 
            'weight', 
            'height', 
            'body_temp', 
            'visit_date'
        ]
        widgets = {

            'visit_date': forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'}),
            'blood_sugar': forms.TextInput(attrs={'class': 'form-control'}),
            'illnes': forms.TextInput(attrs={'class': 'form-control'}),
            'blood_pressure': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.TextInput(attrs={'class': 'form-control'}),
            'height': forms.TextInput(attrs={'class': 'form-control'}),
            'body_temp': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['medication', 'dosage', 'instructions']
        widgets = {
            'medication': forms.Textarea(attrs={'class': 'form-control'}),
            'dosage': forms.Textarea(attrs={'class': 'form-control'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control'}),
        }

class NewPrescriptionForm(forms.ModelForm):
    class Meta:
        model = NewPrescription
        fields = ['medication', 'dosage', 'instructions', 'reason']
        widgets = {
            'medication': forms.Textarea(attrs={'class': 'form-control'}),
            'dosage': forms.Textarea(attrs={'class': 'form-control'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control'}),
        }

class WeeklyReportForm(forms.ModelForm):
    class Meta:
        model = WeeklyReport
        fields = ['duration', 'overview', 'outcomes', 'challenges', 'recommendations', 'conclusion']
        widgets = {
            'duration': forms.TextInput(attrs={'class': 'form-control'}),
            'overview': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'outcomes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'challenges': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'recommendations': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'conclusion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'duration': 'Time Period',
        }

class PrescriptionFeedbackForm(forms.ModelForm):
    class Meta:
        model = PrescriptionFeedback
        fields = ['outcome', 'recommendations']
        widgets = {
            'outcome': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'recommendations': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }