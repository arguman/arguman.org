# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('premises', '0018_premise_supporters'),
    ]

    operations = [
        migrations.AddField(
            model_name='premise',
            name='date_creation',
            field=models.DateTimeField(default=datetime.date(2014, 11, 5), auto_now_add=True),
            preserve_default=False,
        ),
    ]
