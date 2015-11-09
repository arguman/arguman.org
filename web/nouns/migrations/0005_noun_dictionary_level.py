# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nouns', '0004_auto_20151029_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='noun',
            name='dictionary_level',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
