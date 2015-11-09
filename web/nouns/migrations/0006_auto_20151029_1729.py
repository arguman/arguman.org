# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nouns', '0005_noun_dictionary_level'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='noun',
            name='dictionary_level',
        ),
        migrations.RemoveField(
            model_name='noun',
            name='dictionary_offset',
        ),
        migrations.RemoveField(
            model_name='noun',
            name='holonyms',
        ),
        migrations.AddField(
            model_name='noun',
            name='antonyms',
            field=models.ManyToManyField(related_name='antonyms_rel_+', null=True, to='nouns.Noun', blank=True),
            preserve_default=True,
        ),
    ]
