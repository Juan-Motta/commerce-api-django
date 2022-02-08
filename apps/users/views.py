from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import (UserActivateSerializer, UserCreateSerializer,
                          UserListSerializer, UserLoginSerializer,
                          UserSignUpSerializer)


class UserAPIView(APIView):
    """
    Lista y crea usuarios
    """
    def get(self, request):
        user = User.objects.all()
        user_serializer = UserListSerializer(user, many=True)
        return Response(user_serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        user_serializer = UserCreateSerializer(data = request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserActivationAPIView(APIView):
    """
    Activa un usuario
    """
    serializer_class = UserActivateSerializer()
    
    def post(self, request):
        user_serializer = UserActivateSerializer(data = request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({'message': 'Usuario activado correctamente'}, status = status.HTTP_200_OK)
        return Response(user_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(APIView):
    """
    Genera token de acceso de un usuario
    """
    
    def post(self, request):
        #Comprueba las credenciales
        login = UserLoginSerializer(data = request.data)
        if login.is_valid():
            user = login.get_instance()
            if user:
                #Recupera la informacion de usuario y genera el token de acceso
                user_serializer = UserSignUpSerializer(user, context=request.data)
                return Response(user_serializer.data, status=status.HTTP_200_OK)
        return Response(login.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutAPIView(APIView):
    """
    Elimina la informacion del usuario de la cache
    """
    
    def post(self, request, id):
        #Comprueba si el usuario tiene info almacenada en la cache
        if cache.keys(f"user:{id}:*:*").__len__():
            cache.delete(cache.keys(f"user:{id}:*:*")[0])
        return Response({'message': 'Credenciales eliminadas'}, status=status.HTTP_204_NO_CONTENT)