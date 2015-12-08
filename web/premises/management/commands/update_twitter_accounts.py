# coding=utf-8
from django.core.management import BaseCommand

from profiles.models import Profile


class Command(BaseCommand):
    def handle(self, language='en', **kwargs):
        profiles = Profile.objects.all()

        for profile in profiles:
            account = profile.social_auth.filter(provider='twitter').first()

            if account:
                profile.twitter_username = account.user.username
                profile.save()
