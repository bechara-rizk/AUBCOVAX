from django.shortcuts import render, redirect, HttpResponse
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .models import Account
import datetime
from . import scheduling
from datetime import date

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
            today=datetime.datetime.today().strftime('%Y-%m-%d')
            today=date.fromisoformat(today)
            Appt,time=scheduling.getFirstAppointment(today,phone_nbr)
            new=Account.objects.get(phone_nbr=phone_nbr)
            # print(new)
            #scheduling first dose
            new.doseOneDate, new.doseOneTime=Appt,time
            new.save()

            login(request, user)
            return redirect('/patientInfo')
    else:
        form=RegisterForm()
    return render(request, 'register.html', {'form': form})

def patientInfo(request):
    return render(request, 'patientInfo.html')

def medicalSearch(request):
    #TODO add perm
    if request.method == 'POST':
        phoneNb=request.POST.get('phoneNb')
        print(phoneNb)
        return redirect(f'/medicalSearch/{phoneNb}', phoneNb=phoneNb)
    return render(request, 'medicalSearch.html', {'result':False,'nb':''})

def medicalSearchNb(request, phoneNb):
    #TODO add perm
    today=date.fromisoformat(datetime.datetime.today().strftime('%Y-%m-%d'))
    avlbl=[]
    # print(request.POST)
    if request.method == 'POST' and request.POST.get('phoneNb'):
        phoneNb=request.POST.get('phoneNb')
        # print(phoneNb)
        return redirect(f'/medicalSearch/{phoneNb}', phoneNb=phoneNb)
    elif request.method == 'POST' and request.POST.get('confirm'):
        # print(request.POST)
        phoneNb=request.POST.get('confirm') 
        account=Account.objects.get(phone_nbr=phoneNb)
        account.doseOne=True
        account.save()
        return redirect(f'/medicalSearch/{phoneNb}', phoneNb=phoneNb)
    elif request.method == 'POST' and request.POST.get('confirm2'):
        # print(request.POST)
        phoneNb=request.POST.get('confirm2') 
        account=Account.objects.get(phone_nbr=phoneNb)
        account.doseTwo=True
        account.save()
        #TODO generate certificate
        return redirect(f'/medicalSearch/{phoneNb}', phoneNb=phoneNb)
    elif request.method == 'POST' and request.POST.get('view'):
        avlbl=scheduling.viewAvailableAppointmentsRange(today+datetime.timedelta(days=14),7)
        patient=Account.objects.get(phone_nbr=phoneNb)
        context={'result':True ,'patient': patient, 'notFound':False,'nb':phoneNb, 'today':today, 'slots':avlbl}
        return render(request, 'medicalSearch.html', context)
    elif request.method == 'POST' and request.POST.get('date'):
        Date=request.POST.get('date').split()[0]
        Date=date.fromisoformat(Date)
        time=request.POST.get('date').split()[1]
        patient=Account.objects.get(phone_nbr=phoneNb)
        if scheduling.bookAppointment(Date,time,phoneNb):
            patient.doseTwoDate, patient.doseTwoTime=Date, time
            patient.save()
        else:
            return HttpResponse('Error happened please contact site admin')
        return redirect(f'/medicalSearch/{phoneNb}', phoneNb=phoneNb)
    
    patient=Account.objects.filter(phone_nbr=phoneNb)
    try:
        patient=patient[0]
    except:
        return render(request, 'medicalSearch.html', {'result':True, 'notFound':True,'nb':phoneNb})
    
    context={'result':True ,'patient': patient, 'notFound':False,'nb':phoneNb, 'today':today}

    return render(request, 'medicalSearch.html', context)

def adminMed(request):
    if not request.user.is_authenticated or not request.user.isMedicalStaff:
        return render(request, 'notAllowed.html')
    
    personel=Account.objects.filter(isMedicalStaff=True)
    context={'personel':personel}
    return render(request, 'adminMed.html', context)

def adminPatient(request):
    if not request.user.is_authenticated or not request.user.isAdmin:
        return render(request, 'notAllowed.html')
    #TODO
    return render(request, 'adminPatient.html')