from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from .managers import UserManager


class User(AbstractBaseUser):
    """Modelo de usuarios"""
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    nid = models.CharField(max_length=15, unique=True)
    phone = models.CharField(max_length=15, unique=True)
    activation_code = models.IntegerField(null=True)
    is_active = models.BooleanField(default=False)
    profile = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
        'nid'
    ]
    