# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nouns', '0014_auto_20151104_0127'),
        ('premises', '0028_auto_20151102_2154'),
    ]

    operations = [
        migrations.AddField(
            model_name='contention',
            name='related_nouns',
            field=models.ManyToManyField(related_name=b'contentions_related', null=True, to='nouns.Noun', blank=True),
            preserve_default=True,
        ),
    ]
