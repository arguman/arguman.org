from premises.utils import int_or_zero


class PaginationMixin(object):
    def get_offset(self):
        return int_or_zero(self.request.GET.get("offset"))

    def get_limit(self):
        return self.get_offset() + self.paginate_by

    def has_next_page(self):
        total = self.get_contentions(paginate=False).count()
        return total > (self.get_offset() + self.paginate_by)

    def get_next_page_url(self):
        offset = self.get_offset() + self.paginate_by
        return '?offset=%(offset)s' % {
            "offset": offset
        }
