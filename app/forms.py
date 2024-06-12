from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import *

class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.Role.choices)
    first_name=forms.CharField(max_length=200)
    last_name=forms.CharField(max_length=200)
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2','first_name','last_name']

from .models import Notice

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'message']

from django import forms
from .models import StudyMaterial

class StudyMaterialForm(forms.ModelForm):
    class Meta:
        model = StudyMaterial
        fields = ['title', 'description', 'file', 'class_assigned']


class attendanceform(forms.ModelForm):
    class Meta:
        model=attendance
        fields=['subject','status','date']