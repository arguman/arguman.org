# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_auto_20151026_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='karma_point',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
