from django.core.management import BaseCommand
from premises.models import Premise


class Command(BaseCommand):
    def handle(self, *args, **options):
        premises = Premise.objects.all()

        for premise in premises:
            # denormalizes sibling counts
            premise.save()
