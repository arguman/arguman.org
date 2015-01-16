from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions

from profiles.models import Profile
from .serializers import UserProfileSerializer, UserRegisterSerializer


class UserProfileViewset(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserProfileSerializer
    lookup_field = 'username__iexact'
    lookup_url_kwarg = 'username'


class UserRegisterView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserRegisterSerializer
    permissions_classes = (permissions.AllowAny,)


profile_detail = UserProfileViewset.as_view({'get': 'retrieve'})
