from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .models import Account

# Create your views here.

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form=RegisterForm(request.POST)
        # print(form)
        if form.is_valid():
            # print('valid')
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password1')
            name=form.cleaned_data.get('name')
            DOB=form.cleaned_data.get('DOB')
            ID_nbr=form.cleaned_data.get('ID_nbr')
            phone_nbr=form.cleaned_data.get('phone_nbr')
            email=form.cleaned_data.get('email')
            address=form.cleaned_data.get('address')
            medical_history=form.cleaned_data.get('medical_history')
            isMedicalStaff=False
            isAdmin=False

            user=form.save()
            Account.objects.create_user(username, email, password, name=name, DOB=DOB, ID_nbr=ID_nbr, phone_nbr=phone_nbr, address=address, medical_history=medical_history, isMedicalStaff=isMedicalStaff, isAdmin=isAdmin)
            login(request, user)
            return redirect('/')
    else:
        form=RegisterForm()
    return render(request, 'register.html', {'form': form})

def patientInfo(request):
    return render(request, 'patientInfo.html')

def medicalSearch(request):
    if request.method == 'POST':
        phoneNb=request.POST.get('phoneNb')
        print(phoneNb)
        return redirect(f'/medicalSearch/{phoneNb}', phoneNb=phoneNb)
    return render(request, 'medicalSearch.html', {'result':False,'nb':''})

def medicalSearchNb(request, phoneNb):
    if request.method == 'POST':
        phoneNb=request.POST.get('phoneNb')
        print(phoneNb)
        return redirect(f'/medicalSearch/{phoneNb}', phoneNb=phoneNb)
    
    patient=Account.objects.filter(phone_nbr=phoneNb)
    try:
        return render(request, 'medicalSearch.html', {'result':True ,'patient': patient[0], 'notFound':False,'nb':phoneNb})
    except:
        return render(request, 'medicalSearch.html', {'result':True, 'notFound':True,'nb':phoneNb})