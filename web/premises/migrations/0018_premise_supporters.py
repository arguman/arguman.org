# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('premises', '0017_auto_20141030_0353'),
    ]

    operations = [
        migrations.AddField(
            model_name='premise',
            name='supporters',
            field=models.ManyToManyField(related_name=b'supporting', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
