from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.Role.choices)

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']
