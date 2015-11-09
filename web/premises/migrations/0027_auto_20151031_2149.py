# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('premises', '0026_auto_20151028_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contention',
            name='nouns',
            field=models.ManyToManyField(related_name=b'contentions', null=True, to=b'nouns.Noun', blank=True),
        ),
    ]
