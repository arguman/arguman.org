# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('premises', '0005_auto_20141012_0301'),
    ]

    operations = [
        migrations.AddField(
            model_name='contention',
            name='is_published',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
