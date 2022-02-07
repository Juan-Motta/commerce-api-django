from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile
from .serializers import ProfileCreateSerializer, ProfiletListSerializer


class ProfileAPIView(APIView):
    """
    Vista que permite crear o listar todos los perfiles
    """
    def get(self, request):
        #Devuelve una lista con todos los perfiles
        profile = Profile.objects.all()
        profile_serializer = ProfiletListSerializer(profile, many=True)
        return Response(profile_serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        #Crea un perfil en base a la informacion suministrada
        profile_serializer = ProfileCreateSerializer(data = request.data)
        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response(profile_serializer.data, status=status.HTTP_201_CREATED)
        return Response(profile_serializer.error, status=status.HTTP_400_BAD_REQUEST)

class ProfileDetailedAPIView(APIView):
    """
    Vista que permite lista, actualizar un eliminar un perfil en especifico
    """
    def get(self, request):
        #Devuelve un perfil en especifico
        profile = Profile.objects.filter(id=id).first()
        if profile:
            profile_serializer = ProfiletListSerializer(profile)
            return Response(profile_serializer.data, status=status.HTTP_200_OK)
        return Response({'errors': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, id):
        #Actualiza un perfil en especifico
        profile = Profile.objects.filter(id=id).first()
        if profile:
            profile_serializer = ProfileCreateSerializer(instance = profile, data = request.data)
            if profile_serializer.is_valid():
                profile_serializer.save()
                return Response(profile_serializer.data, status = status.HTTP_200_OK)
            return Response(profile_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        return Response({'errors': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, id):
        #Elimina un perfil en especifico
        profile = Profile.objects.filter(id=id).first()
        if profile:
            profile.delete()
            return Response({'message': 'Perfil eliminado correctamente'}, status = status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)