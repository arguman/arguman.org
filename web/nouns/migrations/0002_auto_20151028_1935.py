# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nouns', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noun',
            name='hypernyms',
            field=models.ManyToManyField(related_name=b'hyponyms', null=True, to=b'nouns.Noun', blank=True),
        ),
        migrations.AlterField(
            model_name='noun',
            name='synonyms',
            field=models.ManyToManyField(to=b'nouns.Noun', null=True, blank=True),
        ),
    ]
