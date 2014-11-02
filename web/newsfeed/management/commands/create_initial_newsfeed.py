from django.core.management import BaseCommand
from newsfeed.models import Entry
from premises.models import Contention


class Command(BaseCommand):

    def handle(self, *args, **options):
        for contention in Contention.objects.all():
            Entry.objects.create(
                object_id=contention.id,
                news_type=contention.get_newsfeed_type(),
                sender=contention.get_actor(),
                related_object=contention.get_newsfeed_bundle(),
                date_creation=contention.date_creation
            )
