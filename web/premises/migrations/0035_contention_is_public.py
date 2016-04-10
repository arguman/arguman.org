# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('premises', '0034_contention_community'),
    ]

    operations = [
        migrations.AddField(
            model_name='contention',
            name='is_public',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
