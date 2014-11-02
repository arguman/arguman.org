# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('premises', '0012_auto_20141027_1905'),
    ]

    operations = [
        migrations.AddField(
            model_name='premise',
            name='child_count',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
