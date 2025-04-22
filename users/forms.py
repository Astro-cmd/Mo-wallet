from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
import re

class SignupForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=12,
        help_text="Kenyan number starting with 07, 01, 2547, or 2541"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if not re.match(r'^(0[17]\d{8}|01\d{8}|254[17]\d{7})$', phone):
            raise ValidationError(
                "Enter a valid Kenyan number starting with 07, 01, 2547, or 2541"
            )
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
