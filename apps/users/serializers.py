from django.db import transaction
from django.contrib.auth import password_validation
from django.core.validators import validate_email
from rest_framework import serializers
from .models import User

import random
import re

from .profiles import PROFILES

class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(min_length=1, max_length=30)
    last_name = serializers.CharField(min_length=1, max_length=30)
    nid = serializers.IntegerField()
    phone = serializers.CharField(min_length=7, max_length=15)
    password = serializers.CharField(min_length=5 , max_length=30)
    
    def validate(self, data):
        error_messages = []
        #Validaciones de la contraseña
        try:
            password_validation.validate_password(data['password'], self.instance)
        except Exception as e:
            error_messages.append(list(e.messages))
        #Validaciones del correo
        try:
            validate_email(data['email'])
        except Exception as e:
            error_messages.append(list(e.messages))
        #Validaciones del nid    
        nid_validation = User.objects.filter(nid=data['nid'])
        if nid_validation.__len__():
            error_messages.append({"nid": "Document number already exists"})
        #validaciones del email
        email_validation = User.objects.filter(email=data['email'])
        if email_validation.__len__():
            error_messages.append({"email": "Email already exists"})
        #validaciones de telefono
        phone_validation = self.clean_phone_number(data['phone'])
        if re.match('^[0-9]*$',phone_validation) is None:
            error_messages.append({"phone": "Phone number must have only numbers"})
            
        if error_messages:
            raise ValueError(error_messages)
    
    #Transaction atomic permite realizar los cambios en la db siempre y cuando el codigo se ejecute correctamente, si llega a existir una excepcion, los cambios se revertiran
    @transaction.atomic
    def create(self, data):
        print(data, flush=True)
        data['activation_code'] = self.create_activation_code()
        data['is_active'] = False
        data['profile'] = PROFILES['Cliente']
        user = User.objects.create(**data)
        user.set_password(data['password'])
        user.save()
        return user
        
    def create_activation_code(self):
        return random.randint(1000, 9999)
    
    def clean_phone_number(self, number):
        number = re.sub('\+57|\s|\A57','',number)
        return number
        
    
    
        