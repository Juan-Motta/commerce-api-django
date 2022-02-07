from django.contrib.auth.models import BaseUserManager

from apps.profiles.models import Profile

from .profiles import PROFILES

class UserManager(BaseUserManager):
    """Manager encargados de la creacion de usuarios"""
    def _create_user(self, email, first_name, last_name, nid, phone, profile, password, is_active):
        #Crea una instancia del modelo en base a los parametros ingresados
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            nid=nid,
            is_active=is_active,
            profile=profile,
            phone=phone
        )
        #Crea un password hasheado
        user.set_password(password)
        #Guarda la instancia en base de datos
        user.save(using=self.db)
        return user
    
    # Metodos para definir usuarios y superusuarios, los parametros definidos en los metodos deben corresponder con los campos definidos en el modelo  
    def create_user(self, email, first_name, last_name, nid, phone, password=None):
        return self._create_user(email, first_name, last_name, nid, phone, self._get_profile(PROFILES['Usuario']), password, False)
    
    def create_superuser(self, email, first_name, last_name, nid, phone, password=None):
        return self._create_user(email, first_name, last_name, nid, phone, self._get_profile(PROFILES['Administrador']), password, True)
    
    #Devuelve una instancia de la clase Profile que concuerde con el id
    def _get_profile(self, profile_id):
        return Profile.objects.get(id=profile_id)