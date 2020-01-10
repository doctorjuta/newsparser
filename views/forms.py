"""Forms for parseNews app."""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    """New sign up form based on UserCreationForm class."""
    email = forms.EmailField(max_length=254, help_text="Необхідно. Вкажіть ваш дійсний email.")

    class Meta:
        """Addition data for form."""
        model = User
        fields = ("username", "email", "password1", "password2", )
