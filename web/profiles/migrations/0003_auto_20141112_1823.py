# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.IntegerField(choices=[(0, b'added-premise-for-contention'), (1, b'added-premise-for-premise'), (2, b'reported-as-fallacy'), (3, b'followed'), (4, b'supported-a-premise')]),
        ),
    ]
