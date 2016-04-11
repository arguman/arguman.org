from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response

from newsfeed.models import Entry
from .renderers import MongoDBJSONRenderer
from .mixins import MongoDBPaginationMixin


class NewsfeedViewset(MongoDBPaginationMixin, viewsets.ViewSet):
    renderer_classes = (MongoDBJSONRenderer,)

    def public_newsfeed(self, request):

        community_id = None
        if request.community:
            community_id = request.community.id
        data = Entry.objects.get_public_newsfeed(community_id=community_id,
            **self.get_pagination_context())

        return Response(self.get_paginated_response(data))

    def private_newsfeed(self, request):

        community_id = None
        if request.community:
            community_id = request.community.id

        data = Entry.objects.get_private_newsfeed(community_id=community_id,
            user=self.request.user, **self.get_pagination_context())
        return Response(self.get_paginated_response(data))


public_newsfeed = NewsfeedViewset.as_view(
    {'get': 'public_newsfeed'}
)

private_newsfeed = NewsfeedViewset.as_view(
    {'get': 'private_newsfeed'},
    permission_classes=(permissions.IsAuthenticated,)
)
