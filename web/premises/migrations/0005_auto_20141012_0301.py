# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('premises', '0004_auto_20141012_0056'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contention',
            options={'ordering': ['-date_creation']},
        ),
    ]
