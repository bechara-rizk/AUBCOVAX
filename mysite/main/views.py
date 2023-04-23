from django.shortcuts import render, redirect, HttpResponse
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .models import Account
import datetime
from . import scheduling
from datetime import date
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def sendEmail(subject, message, receiver):
    sender=settings.EMAIL_HOST_USER
    send_mail(subject, message, sender, [receiver], fail_silently=False)

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

            #send email
            subject='Appointment Assignment'
            message=f'''Dear {new.name},
            You have been assigned an appointment for your first dose of the vaccine. Please arrive at the vaccination center at {new.doseOneTime} on {new.doseOneDate}.
            
            Thank you,
            Vaccine Management Team'''
            receiver=new.email
            sendEmail(subject, message, receiver)
            login(request, user)
            return redirect('/patientInfo')
    else:
        form=RegisterForm()
    return render(request, 'register.html', {'form': form})

def patientInfo(request):
    if not request.user.is_authenticated:
        return render(request, 'notAllowed.html')
    return render(request, 'patientInfo.html')

def medicalSearch(request):
    if not request.user.is_authenticated or not request.user.isMedicalStaff:
        return render(request, 'notAllowed.html')
    
    if request.method == 'POST':
        phoneNb=request.POST.get('phoneNb')
        print(phoneNb)
        return redirect(f'/medicalSearch/{phoneNb}', phoneNb=phoneNb)
    patients=Account.objects.filter(isMedicalStaff=False, isAdmin=False, is_superuser=False)
    return render(request, 'medicalSearch.html', {'result':False,'nb':'', 'patients':patients})

def medicalSearchNb(request, phoneNb):
    if not request.user.is_authenticated or not request.user.isMedicalStaff:
        return render(request, 'notAllowed.html')

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
        #send email with certificate
        subject='Vaccine Certificate'
        html_message=render_to_string('certificate.html', {'user':account})
        plain_message=strip_tags(html_message)
        receiver=account.email
        send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [receiver], html_message=html_message, fail_silently=False)
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

            #send email
            subject='Appointment Assignment'
            message=f'''Dear {patient.name},
            You have been assigned an appointment for your second dose of the vaccine. Please arrive at the vaccination center at {patient.doseTwoTime} on {patient.doseTwoDate}.

            Thank you,
            Vaccine Management Team'''
            receiver=patient.email
            sendEmail(subject, message, receiver)
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
    if not request.user.is_authenticated or not request.user.isAdmin:
        return render(request, 'notAllowed.html')
    
    personel=Account.objects.filter(isMedicalStaff=True)
    context={'personel':personel}
    return render(request, 'adminMed.html', context)

def adminPatient(request):
    if not request.user.is_authenticated or not request.user.isAdmin:
        return render(request, 'notAllowed.html')
    results=[]
    context=dict()
    context['found']=True
    if request.method == 'POST':
        if request.POST.get('search-name'):
            # print('name')
            name=request.POST.get('name')
            results=Account.objects.filter(name__icontains=name)
            # print(name)
            context['namefield']=name
        elif request.POST.get('search-phoneNb'):
            # print('phone')
            phoneNb=request.POST.get('phoneNb')
            results=Account.objects.filter(phone_nbr=phoneNb)
            # try:
            #     results=results
            # except:
            #     results=[]
            # print(phoneNb)
            context['nb']=phoneNb
        context['results']=results
        if len(results)==0: context['found']=False

    return render(request, 'adminPatient.html', context)

def viewCertificate(request):
    if not request.user.is_authenticated:
        return render(request, 'notAllowed.html')
    return render(request, 'certificate.html')

def verifyCertificate(request, id):
    # print(id)
    context=dict()
    try:
        account=Account.objects.get(id=id)
    except:
        return render(request, 'verifyCertificate.html', {'notFound':True})
    context['notFound']=False
    context['account']=account
    return render(request, 'verifyCertificate.html', context)