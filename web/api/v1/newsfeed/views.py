from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.templatetags.rest_framework import replace_query_param

from premises.utils import int_or_default
from newsfeed.models import Entry
from .renderers import MongoDBJSONRenderer


class NewsfeedViewset(viewsets.ViewSet):
    """
    Query parameters:
    :param page (integer)
    :param limit (integer)

    For example:
    http://arguman.org/api/v1/newsfeed/public/?page=1
    http://arguman.org/api/v1/newsfeed/public/?page=1&limit=40
    """
    page_query_param = 'page'
    limit_query_param = 'limit'
    renderer_classes = (MongoDBJSONRenderer,)

    def _get_page(self):
        return int_or_default(self.request.GET.get(self.page_query_param), 1)

    def _get_limit(self):
        return int_or_default(self.request.GET.get(self.limit_query_param), 20)

    def _get_pagination_params(self):
        offset = self._get_limit() * (self._get_page() - 1)
        limit = self._get_limit() + offset
        return {
            'offset': offset,
            'limit': limit
        }

    def _get_next_link(self):
        url = self.request.build_absolute_uri()
        return replace_query_param(
            url, self.page_query_param, self._get_page() + 1)

    def _get_previous_link(self):
        url = self.request.build_absolute_uri()
        page = self._get_page()
        if page < 2:
            return None
        return replace_query_param(
            url, self.page_query_param, self._get_page() - 1)

    def get_paginated_response(self, data):
        previous_link = ''
        return {
            'results': data,
            'next': self._get_next_link(),
            'previous': self._get_previous_link()
        }

    def public_newsfeed(self, request):
        data = Entry.objects.get_public_newsfeed(
            **self._get_pagination_params())
        return Response(self.get_paginated_response(data))

    def private_newsfeed(self, request):
        data = Entry.objects.get_private_newsfeed(
            user=self.request.user, **self._get_pagination_params())
        return Response(self.get_paginated_response(data))


public_newsfeed = NewsfeedViewset.as_view(
    {'get': 'public_newsfeed'}
)

private_newsfeed = NewsfeedViewset.as_view(
    {'get': 'private_newsfeed'},
    permission_classes=(permissions.IsAuthenticated,)
)
