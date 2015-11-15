# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nouns', '0017_channel_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='is_featured',
            field=models.BooleanField(default=False, max_length=255),
            preserve_default=True,
        ),
    ]
