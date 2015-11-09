# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('premises', '0027_auto_20151031_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contention',
            name='language',
            field=models.CharField(max_length=5, null=True, choices=[(b'tr', b'tr'), (b'en', b'en'), (b'ch', b'ch')]),
        ),
    ]
