# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('premises', '0013_premise_child_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='premise',
            name='max_sibling_count',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
