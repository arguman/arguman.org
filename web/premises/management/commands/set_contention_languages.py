from django.core.management import BaseCommand

from premises.models import Contention


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        (Contention.objects
         .filter(language__isnull=True)
         .update(language='tr'))
