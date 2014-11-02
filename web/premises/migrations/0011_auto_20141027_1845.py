# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('premises', '0010_auto_20141027_0204'),
    ]

    operations = [
        migrations.AddField(
            model_name='contention',
            name='deleted_at',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contention',
            name='is_deleted',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
