# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_notification_is_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='target_object_id',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
