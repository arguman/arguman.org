# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nouns', '0003_auto_20151028_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='noun',
            name='dictionary_offset',
            field=models.CharField(max_length=25, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='noun',
            name='holonyms',
            field=models.ManyToManyField(related_name=b'meronyms', null=True, to='nouns.Noun', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='noun',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
