# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('premises', '0033_auto_20151115_2230'),
    ]

    operations = [
        migrations.AddField(
            model_name='contention',
            name='is_public',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
