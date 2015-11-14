# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('premises', '0030_report_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='premise',
            name='weight',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
