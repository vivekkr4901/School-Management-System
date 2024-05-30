from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.Role.choices)
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']

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

