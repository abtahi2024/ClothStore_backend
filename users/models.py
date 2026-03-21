from django.db import models
from django.contrib.auth.models import AbstractUser
from users.manager import customUserManager
from cloudinary.models import CloudinaryField
# Create your models here.

class User(AbstractUser):
    username=None
    image=CloudinaryField('profileImage/',blank=True,null=True)
    email=models.EmailField(unique=True)
    address=models.TextField(blank=True,null=True)
    phone_number=models.CharField(max_length=11,blank=True,null=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    objects=customUserManager()
    def __str__(self):
        return self.email or ""