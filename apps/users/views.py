from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User

from .serializers import UserActivateSerializer, UserCreateSerializer, UserListSerializer


class UserAPIView(APIView):
    
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
    
    serializer_class = UserActivateSerializer()
    
    def post(self, request):
        user_serializer = UserActivateSerializer(data = request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({'message': 'Usuario activado correctamente'}, status = status.HTTP_200_OK)
        return Response(user_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
