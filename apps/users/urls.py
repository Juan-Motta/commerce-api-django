from django.urls import path

from .views import UserActivationAPIView, UserAPIView

urlpatterns = [
    path(route='', view=UserAPIView.as_view(), name='users'),
    path(route='activate', view=UserActivationAPIView.as_view(), name='activate_user')
]
