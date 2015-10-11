# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('premises', '0023_auto_20151011_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contention',
            name='ip_address',
            field=models.CharField(max_length=25, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='premise',
            name='ip_address',
            field=models.CharField(max_length=25, null=True, blank=True),
        ),
    ]
