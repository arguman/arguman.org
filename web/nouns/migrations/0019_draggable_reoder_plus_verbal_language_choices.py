# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.translation


class Migration(migrations.Migration):

    dependencies = [
        ('nouns', '0018_channel_is_featured'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='channel',
            options={'ordering': ('order',)},
        ),
        migrations.AlterField(
            model_name='channel',
            name='is_featured',
            field=models.BooleanField(default=False, help_text='If set this channel will be shown on the main page', max_length=255),
        ),
        migrations.AlterField(
            model_name='channel',
            name='language',
            field=models.CharField(default=django.utils.translation.get_language, max_length=255, choices=[(b'tr', 'T\xfcrk\xe7e'), (b'en', 'English'), (b'ch', '\u4e2d\u6587'), (b'fr', 'Fran\xe7ais')]),
        ),
        migrations.AlterField(
            model_name='channel',
            name='order',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='noun',
            name='language',
            field=models.CharField(default=django.utils.translation.get_language, max_length=25, choices=[(b'tr', 'T\xfcrk\xe7e'), (b'en', 'English'), (b'ch', '\u4e2d\u6587'), (b'fr', 'Fran\xe7ais')]),
        ),
    ]
