# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('premises', '0027_auto_20151028_2210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='premise',
            name='user',
            field=models.ForeignKey(related_name=b'user_premises', to=settings.AUTH_USER_MODEL),
        ),
    ]
