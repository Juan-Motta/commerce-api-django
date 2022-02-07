from django.urls import path

from .views import ProfileAPIView, ProfileDetailedAPIView

urlpatterns = [
    path(route='', view=ProfileAPIView.as_view(), name='profiles'),
    path(route='<int:id>', view=ProfileDetailedAPIView.as_view(), name='profile_detailed'),
]