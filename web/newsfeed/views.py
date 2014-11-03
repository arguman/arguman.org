from django.views.generic import View, TemplateView
from newsfeed.constants import NEWS_TYPE_CONTENTION, NEWS_TYPE_PREMISE, NEWS_TYPE_FALLACY, NEWS_TYPE_FOLLOWING
from newsfeed.models import Entry
from premises.utils import int_or_zero
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
            newsfeed = self.get_private_newsfeed()
        else:
            newsfeed = self.get_public_newsfeed()
        return newsfeed

    def has_next_page(self):
        # tricky a little bit.
        # if the page loaded full, probably there are more news
        # entries. if not, returns a single empty page, it's not a problem.
        # it's more effortless instead of get all collection for now.
        return (len(self.get_news_entries()) == self.paginate_by)

    def get_private_newsfeed(self):
        """
        Fetches news items from the newsfeed database
        """
        parameters = {
            "recipients": {
                "$in": [self.request.user.id]
            },
            "news_type": {
                "$in": [NEWS_TYPE_CONTENTION,
                        NEWS_TYPE_PREMISE,
                        NEWS_TYPE_FALLACY,
                        NEWS_TYPE_FOLLOWING]
        }}

        newsfeed = (Entry
                    .objects
                    .collection
                    .find(parameters)
                    .sort([("date_created", -1)])
                    .skip(self.get_offset())
                    .limit(self.paginate_by))

        return map(Entry, newsfeed)

    def get_public_newsfeed(self):
        """
        Fetches news items from the newsfeed database
        """
        parameters = {
            "news_type": {
                "$in": [NEWS_TYPE_CONTENTION,
                        NEWS_TYPE_PREMISE]
        }}

        newsfeed = (Entry
                    .objects
                    .collection
                    .find(parameters)
                    .sort([("date_created", -1)])
                    .skip(self.get_offset())
                    .limit(self.paginate_by))

        return map(Entry, newsfeed)


class PublicNewsfeedView(NewsfeedView):
    get_news_entries = NewsfeedView.get_public_newsfeed

    def get_context_data(self, **kwargs):
        return super(PublicNewsfeedView, self).get_context_data(
            newsfeed_is_public=True,
            **kwargs)
