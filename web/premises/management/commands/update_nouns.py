# coding=utf-8
from django.core.management import BaseCommand

from premises.models import Contention


class Command(BaseCommand):
    def handle(self, language='en', **kwargs):
        contentions = Contention.objects.filter(language=language)

        Contention.nouns.through.objects.all().delete()

        for contention in contentions:
            contention.save_nouns()
            print contention.title, contention.nouns.all()
