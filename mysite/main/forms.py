from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Account

class RegisterForm(UserCreationForm):
    #add fields other than username and password
    name = forms.CharField(max_length=200, label='Full Name')
    DOB = forms.DateField(label='Date of Birth, MM/DD/YYYY')
    ID_nbr = forms.IntegerField(label="ID Number")
    phone_nbr = forms.IntegerField(label="Phone Number")
    email = forms.EmailField(label="Email Address")
    address = forms.CharField(max_length=200, label="Address, city and country")
    medical_history = forms.CharField(max_length=2000, widget=forms.Textarea)

    class Meta:
        model=Account
        #add fields in order of appearance including username, password, and password2
        fields=['name', 'DOB', 'ID_nbr', 'phone_nbr', 'email', 'address', 'medical_history', 'username', 'password1', 'password2']