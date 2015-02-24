from rest_framework import viewsets
from rest_framework import permissions


class NewsfeedViewset(viewsets.ViewSet):

    def public_newsfeed(self, request):
        pass

    def private_newsfeed(self, request):
        pass


public_newsfeed = NewsfeedViewset.as_view(
    {'get': 'public_newsfeed'}
)

private_newsfeed = NewsfeedViewset.as_view(
    {'get': 'private_newsfeed'},
    permission_classes=(permissions.IsAuthenticated,)
)
