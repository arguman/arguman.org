# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('premises', '0025_auto_20151011_2241'),
    ]

    operations = [
        migrations.AddField(
            model_name='contention',
            name='score',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
