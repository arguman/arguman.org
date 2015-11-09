# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nouns', '0012_auto_20151102_2209'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='keyword',
            name='is_visible',
        ),
    ]
