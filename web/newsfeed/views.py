from newsfeed.models import Entry
from premises.views import HomeView


class NewsfeedView(HomeView):
    tab_class = "newsfeed"
    template_name = "newsfeed.html"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        return super(NewsfeedView, self).get_context_data(
            news_entries=self.get_news_entries(),
            **kwargs)

    def get_news_entries(self):
        if self.request.user.is_authenticated():
            newsfeed = Entry.objects.get_private_newsfeed(
                offset=self.get_offset(), limit=self.paginate_by,
                user=self.request.user)
        else:
            newsfeed = Entry.objects.get_public_newsfeed(
                offset=self.get_offset(), limit=self.paginate_by)
        return newsfeed

    def has_next_page(self):
        # tricky a little bit.
        # if the page loaded full, probably there are more news
        # entries. if not, returns a single empty page, it's not a problem.
        # it's more effortless instead of get all collection for now.
        return (len(self.get_news_entries()) == self.paginate_by)


class PublicNewsfeedView(NewsfeedView):
    def get_news_entries(self):
        return Entry.objects.get_public_newsfeed(
            offset=self.get_offset(), limit=self.paginate_by)

    def get_context_data(self, **kwargs):
        return super(PublicNewsfeedView, self).get_context_data(
            newsfeed_is_public=True,
            **kwargs)
