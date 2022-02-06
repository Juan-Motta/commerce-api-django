from django.db import models

class Profile(models.Model):
    """Modelo de perfiles de usuario"""
    name = models.CharField(max_length=30)
