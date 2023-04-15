from django.db import models
from django.contrib.auth.models import AbstractUser,User, UserManager, AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        username = self.model.normalize_username(username)
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        if extra_fields.get('is_superuser') == True:
            user.save()
        return user
    
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(username, email, password, **extra_fields)

class Account(AbstractBaseUser, PermissionsMixin):
    # user=models.OneToOneField(User, on_delete=models.CASCADE)
    username=models.CharField(max_length=200, unique=True)

    isMedicalStaff = models.BooleanField(default=False)
    isAdmin = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=False)
    DOB = models.DateField()
    ID_nbr = models.IntegerField(unique=True)
    phone_nbr = models.IntegerField()
    address = models.CharField(max_length=200)
    medical_history = models.TextField()
    doseOne = models.BooleanField(default=False)
    doseOneDate = models.DateField(null=True, blank=True)
    doseTwo = models.BooleanField(default=False)
    doseTwoDate = models.DateField(null=True, blank=True)
    nextAppointment = models.DateField(null=True, blank=True)

    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'email', 'isMedicalStaff', 'isAdmin', 'DOB', 'ID_nbr', 'phone_nbr', 'address', 'medical_history']

    def __str__(self):
        return self.username