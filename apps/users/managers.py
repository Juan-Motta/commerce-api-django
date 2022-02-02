from django.contrib.auth.models import BaseUserManager

from .profiles import PROFILES

class UserManager(BaseUserManager):
    """Manager encargados de la creacion de usuarios"""
    def _create_user(self, email, first_name, last_name, nid, profile, password, is_active):
        #Crea una instancia del modelo en base a los parametros ingresados
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            nid=nid,
            is_active=is_active,
            profile=profile,
        )
        #Crea un password hasheado
        user.set_password(password)
        #Guarda la instancia en base de datos
        user.save(using=self.db)
        return user
    
    # Metodos para definir usuarios y superusuarios, los parametros definidos en los metodos deben corresponder con los campos definidos en el modelo  
    def create_user(self, email, first_name, last_name, nid, password=None):
        return self._create_user(email, first_name, last_name, nid, password, False)
    
    def create_superuser(self, email, first_name, last_name, nid, password=None):
        return self._create_user(email, first_name, last_name, nid, PROFILES['Administrador'], password, True)