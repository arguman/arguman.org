# coding=utf-8
from django.core.management import BaseCommand

from nouns.models import Noun


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Noun.objects.update(language='en')
