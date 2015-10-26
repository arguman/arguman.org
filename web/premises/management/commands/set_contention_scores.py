from django.core.management import BaseCommand

from premises.models import Contention


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        contentions = Contention.objects.all()
        for contention in contentions:
            score = contention.calculate_score()
            contention.score = score
            print contention.title, ' == ', contention.score
            contention.save(skip_date_update=True)