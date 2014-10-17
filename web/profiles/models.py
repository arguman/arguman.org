from django.contrib.auth.models import AbstractUser
from django.db import models


class Profile(AbstractUser):
    following = models.ManyToManyField("self", symmetrical=False)

    @property
    def followers(self):
        # todo: find a way to make reverse relationships
        # with symmetrical false option
        return Profile.objects.filter(following=self)
