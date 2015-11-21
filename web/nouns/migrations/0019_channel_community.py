# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '__first__'),
        ('nouns', '0018_channel_is_featured'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='community',
            field=models.ForeignKey(blank=True, to='communities.Community', null=True),
            preserve_default=True,
        ),
    ]
