from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.db import transaction
import datetime
from college.models import College, Department, Course, Specialization
from accounts.models import Alumni, Faculty, User
from PIL import Image


def year_choices():
    return [(r, r) for r in range(1947, datetime.date.today().year + 1)]


class AlumniSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    college = forms.ModelChoiceField(queryset=College.objects.all(), required=True)
    unique_id = forms.CharField(max_length=200)
    email = forms.EmailField()
    image = forms.ImageField()
    phone = forms.CharField(max_length=20)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_alumni = True
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.full_name = self.cleaned_data['first_name'] + " " + self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.college = College.objects.get(name=self.cleaned_data['college'])
        user.profile_photo = self.cleaned_data['image']
        user.phone = self.cleaned_data['phone']
        user.save()
        unique_id = self.cleaned_data['unique_id']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        email_address = self.cleaned_data['email']
        system_date_joined = datetime.datetime.now()

        alumni = Alumni.objects.create(
            user=user,
            unique_id=unique_id,
        )
        return user


class FacultySignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    college = forms.ModelChoiceField(queryset=College.objects.all(), required=True)
    email = forms.EmailField()
    image = forms.ImageField()
    phone = forms.CharField(max_length=20)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_faculty = True
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.full_name = self.cleaned_data['first_name'] + " " + self.cleaned_data['last_name']
        user.college = College.objects.get(name=self.cleaned_data['college'])
        user.profile_photo = self.cleaned_data['image']
        user.phone = self.cleaned_data['phone']
        user.save()
        system_date_joined = datetime.datetime.now()

        faculty = Faculty.objects.create(user=user, )
        return user


class CompleteAlumniProfile(forms.ModelForm):

    course_choices = Course.objects.all()
    department_choices = Department.objects.all()
    specialization_choices = Specialization.objects.all()

    course = forms.ModelChoiceField(queryset=course_choices, required=True)
    department = forms.ModelChoiceField(queryset=department_choices, required=False)
    specialization = forms.ModelChoiceField(queryset=specialization_choices, required=False)
    dob = forms.DateField()
    year_of_passing = forms.ChoiceField(choices=year_choices())
    location = forms.CharField(max_length=200, required=True)
    facebook_profile = forms.URLField(max_length=1000, required=False)
    twitter_profile = forms.URLField(max_length=1000, required=False)
    linkedin_profile = forms.URLField(max_length=1000, required=False)
    about_me = forms.CharField(max_length=1000, widget=forms.TextInput({}), required=False)

    class Meta:
        model = Alumni
        fields = ('dob', 'course', 'department', 'specialization', 'location', 'facebook_profile', 'twitter_profile',
                  'linkedin_profile', 'about_me')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(CompleteAlumniProfile, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user = self.user
        alumni = Alumni.objects.get(user=self.user)

        department = self.cleaned_data['department']
        if department:
            user.department = Department.objects.get(name=self.cleaned_data['department'])

        course = self.cleaned_data['course']
        if course:
            user.course = Course.objects.get(name=self.cleaned_data['course'])

        specialization = self.cleaned_data['specialization']
        if specialization:
            user.specialization = Specialization.objects.get(name=self.cleaned_data['specialization'])

        user.dob = self.cleaned_data['dob']
        alumni.year_of_passing = self.cleaned_data['year_of_passing']
        user.facebook_profile = self.cleaned_data['facebook_profile']
        user.twitter_profile = self.cleaned_data['twitter_profile']
        user.linkedin_profile = self.cleaned_data['linkedin_profile']
        user.about_me = self.cleaned_data['about_me']
        user.location = self.cleaned_data['location']
        user.profile_complete = 1
        alumni.save()
        user.save()


class CompleteFacultyProfile(forms.ModelForm):

    course_choices = Course.objects.all()
    department_choices = Department.objects.all()
    specialization_choices = Specialization.objects.all()

    course = forms.ModelChoiceField(queryset=course_choices, required=True)
    department = forms.ModelChoiceField(queryset=department_choices, required=False)
    specialization = forms.ModelChoiceField(queryset=specialization_choices, required=False)
    dob = forms.DateField()
    college_joined_year = forms.ChoiceField(choices=year_choices())
    research_interest = forms.CharField(max_length=300)
    facebook_profile = forms.URLField(max_length=1000, required=False)
    twitter_profile = forms.URLField(max_length=1000, required=False)
    linkedin_profile = forms.URLField(max_length=1000, required=False)
    about_me = forms.CharField(max_length=1000, widget=forms.TextInput({}), required=False)

    class Meta:
        model = Alumni
        fields = ('dob', 'department', 'college_joined_year', 'research_interest')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(CompleteFacultyProfile, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user = self.user
        faculty = Faculty.objects.get(user=self.user)

        department = self.cleaned_data['department']
        if department:
            user.department = Department.objects.get(name=self.cleaned_data['department'])

        course = self.cleaned_data['course']
        if course:
            user.course = Course.objects.get(name=self.cleaned_data['course'])

        specialization = self.cleaned_data['specialization']
        if specialization:
            user.specialization = Specialization.objects.get(name=self.cleaned_data['specialization'])

        user.dob = self.cleaned_data['dob']
        faculty.college_joined_year = self.cleaned_data['college_joined_year']
        faculty.research_interest = self.cleaned_data['research_interest']
        user.facebook_profile = self.cleaned_data['facebook_profile']
        user.twitter_profile = self.cleaned_data['twitter_profile']
        user.linkedin_profile = self.cleaned_data['linkedin_profile']
        user.about_me = self.cleaned_data['about_me']
        user.profile_complete = 1
        faculty.save()
        user.save()


class AccountAuthenticationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid Login")


class UpdateAlumniProfile(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'college', 'dob')
