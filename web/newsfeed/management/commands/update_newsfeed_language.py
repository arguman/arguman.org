from django.core.management import BaseCommand
from premises.models import Contention, Premise
from newsfeed.models import Entry
from newsfeed.constants import (
    NEWS_TYPE_CONTENTION, NEWS_TYPE_PREMISE,
    NEWS_TYPE_FALLACY, NEWS_TYPE_FOLLOWING)

RELATED_MODELS = {
    NEWS_TYPE_CONTENTION: Contention,
    NEWS_TYPE_PREMISE: Premise,
}


class Command(BaseCommand):

    def handle(self, *args, **options):
		entries = Entry.objects.collection.find({
		    "news_type": {
		        "$in": [NEWS_TYPE_CONTENTION,
		                NEWS_TYPE_PREMISE]
		    }
		})

		for entry in entries:
   			model = RELATED_MODELS[entry['news_type']]
			try:
				instance = model.objects.get(id=entry['object_id'])
			except model.DoesNotExist:
				continue
			
			Entry.objects.collection.update({
				'_id': entry['_id']
			}, {
				"$set": {
					"related_object": instance.get_newsfeed_bundle()
				}
			}, multi=True)


			
