from rest_framework import viewsets
from rest_framework import permissions

from profiles.models import Profile
from .serializers import UserProfileSerializer


class UserProfileViewset(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserProfileSerializer
    lookup_field = 'username'
    lookup_url_kwarg = 'username'


profile_detail = UserProfileViewset.as_view({'get': 'retrieve'})
