# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('premises', '0026_contention_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contention',
            name='date_modification',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
