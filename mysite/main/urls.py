from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('patientInfo/', views.patientInfo, name='patientInfo'),
    path('medicalSearch/', views.medicalSearch, name='medicalSearch'),
    path('medicalSearch/<int:phoneNb>', views.medicalSearchNb, name='medicalSearch'),
    path('adminMed/', views.adminMed, name='adminMed'),
    path('adminPatient/', views.adminPatient, name='adminPatient'),
    path('viewCertificate/', views.viewCertificate, name='viewCertificate'),
    # path('verifyCertificate/', views.viewCertificate, name='viewCertificate'),
    path('verifyCertificate/<int:id>', views.verifyCertificate, name='verifyCertificate'),
    path('downCertificate/', views.downCertificate, name='downCertificate'),
    path('stats/', views.stats, name='stats'),
]