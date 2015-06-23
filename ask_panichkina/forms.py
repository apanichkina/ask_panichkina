from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from ask_panichkina.models import *
from django.contrib.auth.models import User
from django import forms



class SignupForm(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirmation = forms.CharField(widget=forms.PasswordInput())
    avatar = forms.ImageField(required=False)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('This username is already exists')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            validate_email(email)
            return email
        except ValidationError:
            raise forms.ValidationError('Incorrect email')

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        password = cleaned_data['password']
        password_confirmation = cleaned_data['password_confirmation']
        if password != password_confirmation:
            errormsg = 'Passwords do not match'
            self._errors["password_confirmation"] = self.error_class([errormsg])
        return cleaned_data





