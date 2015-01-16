from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import detail_route
from rest_framework import status
from rest_framework.response import Response

from profiles.models import Profile
from .serializers import UserProfileSerializer, UserRegisterSerializer
from profiles.signals import follow_done, unfollow_done


class UserProfileViewset(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = UserProfileSerializer
    lookup_field = 'username__iexact'
    lookup_url_kwarg = 'username'

    @detail_route(methods=['post'])
    def follow(self, request, username=None):
        user = self.get_object()
        if user.id == request.user.id:
            return Response({'message': "Kedini takip edemezsin."},
                            status=status.HTTP_400_BAD_REQUEST)

        if user.followers.filter(pk=request.user.pk).exists():
            return Response({'message': "Zaten bu kullaniciyi takip ediyorsun"},
                            status=status.HTTP_400_BAD_REQUEST)

        request.user.following.add(user)
        follow_done.send(sender=self, follower=request.user, following=user)
        return Response(status=status.HTTP_201_CREATED)

    @detail_route(methods=['delete'])
    def unfollow(self, request, username=None):
        user = self.get_object()
        if not request.user.following.filter(id=user.id).exists():
            return Response(
                {'message': "Takibi birakmadan once takip etmen gerekiyor."},
                status=status.HTTP_400_BAD_REQUEST)

        request.user.following.remove(user)
        unfollow_done.send(sender=self, follower=request.user, following=user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @detail_route(methods=['get'])
    def followings(self, request, username=None):
        user = self.get_object()
        page = self.paginate_queryset(user.following.all())
        serializer = self.get_pagination_serializer(page)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def followers(self, request, username=None):
        user = self.get_object()
        page = self.paginate_queryset(user.followers.all())
        serializer = self.get_pagination_serializer(page)
        return Response(serializer.data)


class UserRegisterView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserRegisterSerializer
    permissions_classes = (permissions.AllowAny,)


profile_detail = UserProfileViewset.as_view({'get': 'retrieve'})
profile_followers = UserProfileViewset.as_view({'get': 'followers'})
profile_followings = UserProfileViewset.as_view({'get': 'followings'})
profile_follow = UserProfileViewset.as_view({'post': 'follow',
                                             'delete': 'unfollow'})
