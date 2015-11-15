# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('premises', '0032_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contention',
            name='channel',
        ),
        migrations.DeleteModel(
            name='Channel',
        ),
    ]
