import random
import re

from django.contrib.auth import password_validation
from django.core.validators import validate_email
from django.db import transaction
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from apps.profiles.serializers import ProfiletListSerializer
from .profiles import PROFILES


class UserCreateSerializer(serializers.Serializer):
    """
    Serializador para la creacion de usuarios
    Recibe en el request el email, nombres, apellidos, nid, telefono y contraseña. 
    Valida que los datos ingresados son correctos mediante los metodos validate y crea el usuario en el metodo create
    """

    email = serializers.EmailField()
    first_name = serializers.CharField(min_length=1, max_length=30)
    last_name = serializers.CharField(min_length=1, max_length=30)
    nid = serializers.CharField(max_length=15)
    phone = serializers.CharField(min_length=7, max_length=15)
    password = serializers.CharField(min_length=5, max_length=30)

    def validate_password(self, password):
        # Validaciones de la contraseña
        try:
            password_validation.validate_password(password, self.instance)
            return password
        except Exception as error:
            #el objeto error puede contener multiples errores, por ellos se debe convertir a una lista
            raise serializers.ValidationError(list(error))

    def validate_email(self, email):
        # Validaciones del correo
        try:
            validate_email(email)
            email_validation = User.objects.filter(email=email)
            if email_validation.__len__():
                raise self.ValidationError("El email ya existe.")
            return email
        except Exception as error:
            #el objeto error puede contener multiples errores, por ellos se debe convertir a una lista
            raise serializers.ValidationError(list(error))

    def validate_nid(self, nid):
        # Validaciones de nid
        nid_validation = User.objects.filter(nid=nid)
        if nid_validation.__len__():
            raise serializers.ValidationError("El documento ya existe.")
        return nid

    def validate_phone(self, phone):
        # Validaciones de telefono
        phone_validation = User.objects.filter(phone=phone)
        if phone_validation.__len__():
            raise serializers.ValidationError("El numero de telefono ya existe.")
        phone_validation = self.clean_phone_number(phone)
        if re.match('^[0-9]*$', phone_validation) is None:
            raise serializers.ValidationError("El numero de telefono solo debe contener numeros.")
        return phone

    # Transaction atomic permite realizar los cambios en la db siempre y cuando el codigo se ejecute correctamente, si llega a existir una excepcion, los cambios se revertiran
    @transaction.atomic
    def create(self, data):
        data['activation_code'] = self.create_activation_code()
        data['is_active'] = False
        data['profile'] = PROFILES['Cliente']
        user = User.objects.create(**data)
        user.set_password(data['password'])
        user.save()
        return user

    def create_activation_code(self):
        # Crea un codigo de activacion de 4 digitos
        return random.randint(1000, 9999)

    def clean_phone_number(self, number):
        # Elimina +57, 57 y los espacios del numero de telefono
        number = re.sub('\+57|\s|\A57', '', number)
        return number

class UserActivateSerializer(serializers.Serializer):
    """
    Serializador para la activacion de usuarios. Recibe el id de usuario y un codigo, compara el codigo del usuario con el codigo proporcionado y activa la cuenta
    """
    user_id = serializers.IntegerField()
    activation_code = serializers.IntegerField()
    
    def validate_user_id(self, user_id):
        #Valida que el usuario existe
        user = User.objects.filter(id=user_id)
        if not user:
            raise serializers.ValidationError(f'No existe un usuario con el id {user_id}.')
        return user_id

    def validate_activation_code(self, activation_code):
        #Valida que el codigo proporcionado sea correcto
        if activation_code < 1000 or activation_code > 9999:
            raise serializers.ValidationError("El codigo de activacion solo debe contener numeros.")
        return activation_code
        
    def create(self, data):
        #Se garantiza que el usuario existe debido a la validacion del user_id
        user = User.objects.filter(id = data['user_id'])[0]
        if user.activation_code == data['activation_code']:
            user.is_active = True
            user.save()
            return data
        raise serializers.ValidationError({'activation_code': 'El codigo de activacion es incorrecto.'})    

        
class UserListSerializer(serializers.Serializer):
    """
    Serializador para el listado de usuarios
    """
    id = serializers.IntegerField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    nid = serializers.CharField()
    phone = serializers.CharField()
    is_active = serializers.BooleanField()
    profile = serializers.IntegerField()
    
    def to_representation(self, instance):
        #Modifica el id del perfil por el nombre del perfil
        data = super().to_representation(instance)
        data['profile'] = list(PROFILES.keys())[data['profile']-1]
        return data
    

class UserLoginSerializer(serializers.Serializer):
    """
    Serializador que valida las credenciales de usuario y devuelve el 1 del usuario
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    
    def validate_username(self, username):
        #Si el usuarname es email
        if '@' in username:
            user = User.objects.filter(email=username).first()
            if user:
                self.context['user'] = user
                return username
        #Si el username es telefono
        user = User.objects.filter(phone=username).first()
        if user:
            self.context['user'] = user
            return username
        raise serializers.ValidationError("Usuario o contraseña incorrectos")
    
    def validate_password(self, password):
        #Valida si la contraseña proporsionada coincide con la contraseña del usuario
        user = self.context['user']
        if user.check_password(password):
            return password
        raise serializers.ValidationError("Usuario o contraseña incorrectos")
    
    def to_representation(self, instance):
        #Si las validaciones son correctas devuelve el id del usuario en forma de diccionario
        return {'id': self.context['user'].id}

class UserSignUpSerializer(serializers.Serializer):
    """
    Serializador que devuelve la informacion del usuario mas un token de acceso
    """
    id = serializers.IntegerField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    nid = serializers.CharField()
    phone = serializers.CharField()
    is_active = serializers.BooleanField()
    profile = ProfiletListSerializer()
    token = serializers.CharField(required=False)
    
    def to_representation(self, instance):
        token = None
        #Comprueba que la contraseña corresponde a la del usuario
        if instance.check_password(self.context['password']):
                token = self._get_token(instance)
        data = super().to_representation(instance)
        data['token'] = token
        return data
    
    def _get_token(self, user):
        #Devuelve un token asociado al usuario
        tokens = RefreshToken.for_user(user)
        return {
            'access': str(tokens.access_token)
        }