from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User

from .serializers import UserActivateSerializer, UserCreateSerializer, UserListSerializer, UserLoginSerializer, UserSignUpSerializer


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
            #Busca un usuario con el id entregado por el serializador  
            user = User.objects.filter(id=login.data['id']).first()
            if user:
                #Recupera la informacion de usuario y genera el token de acceso
                user_serializer = UserSignUpSerializer(user, context=request.data)
                return Response(user_serializer.data, status=status.HTTP_200_OK)
    