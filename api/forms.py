from dataclasses import field
from pyexpat import model
from django import forms
from .models import User


class PasswordResetForm(forms.Form):
    
    password1 = forms.CharField()
    password2 = forms.CharField()
