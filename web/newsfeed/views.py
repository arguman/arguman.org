from newsfeed.constants import NEWS_TYPE_CONTENTION, NEWS_TYPE_PREMISE, NEWS_TYPE_FALLACY, NEWS_TYPE_FOLLOWING
from newsfeed.models import Entry
from premises.views import HomeView


class NewsfeedView(HomeView):
    tab_class = "newsfeed"
    template_name = "newsfeed.html"

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated():
            newsfeed = self.get_private_newsfeed()
        else:
            newsfeed = self.get_public_newsfeed()
        return super(NewsfeedView, self).get_context_data(
            news_entries=newsfeed,
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
                    .sort([("date_created", -1)])
                    .skip(offset)
                    .limit(limit))

        return map(Entry, newsfeed)

    def get_public_newsfeed(self, offset=0, limit=40):
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
                    .skip(offset)
                    .limit(limit))

        return map(Entry, newsfeed)


class PublicNewsfeedView(NewsfeedView):
    def get_context_data(self, **kwargs):
        return super(NewsfeedView, self).get_context_data(
            news_entries=self.get_public_newsfeed(),
            newsfeed_is_public=True,
            **kwargs)
