# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('premises', '0003_premise_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='contention',
            name='date_creation',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 12, 0, 56, 45, 227936), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contention',
            name='slug',
            field=models.SlugField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='premise',
            name='argument',
            field=models.ForeignKey(related_name=b'premises', to='premises.Contention'),
        ),
    ]
