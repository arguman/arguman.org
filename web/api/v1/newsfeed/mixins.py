from rest_framework.templatetags.rest_framework import replace_query_param
from premises.utils import int_or_default


class MongoDBPaginationMixin(object):
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

    def get_page(self):
        return int_or_default(self.request.GET.get(self.page_query_param), 1)

    def get_limit(self):
        return int_or_default(self.request.GET.get(self.limit_query_param), 20)

    def get_pagination_context(self):
        offset = self.get_limit() * (self.get_page() - 1)
        limit = self.get_limit() + offset
        return {
            'offset': offset,
            'limit': limit
        }

    def get_next_link(self):
        url = self.request.build_absolute_uri()
        return replace_query_param(
            url, self.page_query_param, self.get_page() + 1)

    def get_previous_link(self):
        url = self.request.build_absolute_uri()
        page = self.get_page()
        if page < 2:
            return None
        return replace_query_param(
            url, self.page_query_param, self.get_page() - 1)

    def get_paginated_response(self, data):
        return {
            'results': data,
            'next': self.get_next_link(),
            'previous': self.get_previous_link()
        }
