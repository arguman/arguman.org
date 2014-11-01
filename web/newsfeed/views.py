from newsfeed.constants import NEWS_TYPE_CONTENTION, NEWS_TYPE_PREMISE, NEWS_TYPE_FALLACY, NEWS_TYPE_FOLLOWING
from newsfeed.models import Entry
from premises.views import HomeView


class NewsfeedView(HomeView):
    tab_class = "newsfeed"
    template_name = "newsfeed.html"

    def get_context_data(self, **kwargs):
        return super(NewsfeedView, self).get_context_data(
            news_entries=self.get_private_newsfeed(),
            **kwargs)

    def get_private_newsfeed(self, offset=0, limit=40):
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
                    .sort([("date_created", -1)]))

        return map(Entry, newsfeed[offset:offset + limit])
