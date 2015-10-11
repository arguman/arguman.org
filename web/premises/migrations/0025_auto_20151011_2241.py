# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('premises', '0024_auto_20151011_2239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contention',
            name='ip_address',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='premise',
            name='ip_address',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
