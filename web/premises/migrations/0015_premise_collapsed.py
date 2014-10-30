# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('premises', '0014_premise_max_sibling_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='premise',
            name='collapsed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
