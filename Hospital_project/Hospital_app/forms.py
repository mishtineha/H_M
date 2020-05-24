from django.forms import ModelForm
from django import forms
from Hospital_app.models import Doctor,Patient
from django.contrib.auth.models import User

class Login(ModelForm):
    class Meta:
        model = User
        fields = ['username','password']

class Signin_doctor(forms.Form):
    Name = forms.CharField(max_length=1500)
    username = forms.CharField(max_length=1500)
    Email = forms.EmailField()
    gender = forms.CharField(max_length=1500)
    phone_no = forms.IntegerField()
    Degree = forms.CharField(max_length=1500)
    specialization = forms.CharField(max_length=1500)
    password = forms.CharField(max_length=20,widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=20,widget=forms.PasswordInput)

class Signin_patient(forms.Form):
    Name = forms.CharField(max_length=1500)
    username = forms.CharField(max_length=1500)
    Email = forms.EmailField()
    gender = forms.CharField(max_length=1500)
    phone_no = forms.IntegerField()
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=20, widget=forms.PasswordInput)

