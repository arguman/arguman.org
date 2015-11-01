# coding=utf-8
from django.core.management import BaseCommand

from premises.models import Contention


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        contentions = Contention.objects.all()

        for contention in contentions:
            contention.nouns.clear()
            contention.save_nouns()
