from django.core.management import BaseCommand
from django.db.models import Count, Sum
from premises.models import Premise
from profiles.models import Profile


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = Profile.objects.all()
        for user in users:
            # Calculate the support count
            karma = user.calculate_karma()
            user.karma = karma
            user.save()
            # print user.username, '==', user.karma
