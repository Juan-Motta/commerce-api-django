from django.core.cache import cache
from .models import User

def _get_user(id=None,email=None,phone=None):
    """Recupera el usuario del cache en base al parametro entregado, si no existe el usuario lo recupera de db y lo guarda en cache"""
    if id:    
        user = cache.get(f"user:{id}:*:*")
        if user:
            return user
        user = User.objects.filter(id=id).first()
    if email:    
        user = cache.get(f"user:*:{email}:*")
        if user:
            return user
        user = User.objects.filter(email=email).first()
    if phone:    
        user = cache.get(f"user:*:*:{phone}")
        if user:
            return user
        user = User.objects.filter(phone=phone).first()
    if user:
        cache.set(f"user:{user.id}:{user.email}:{user.phone}", user, timeout=86400)
        return user
    return None
