from django.urls import path

from .views import UserAPIView

urlpatterns = [
    path(route='', view=UserAPIView.as_view(), name='users')
]