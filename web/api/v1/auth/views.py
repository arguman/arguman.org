from rest_framework import generics
from rest_framework import permissions

from .serializers import UserRegisterSerializer
from profiles.models import Profile


class UserRegisterView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserRegisterSerializer
    permissions_classes = (permissions.AllowAny,)
