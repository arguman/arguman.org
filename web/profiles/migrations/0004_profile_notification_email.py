# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20141112_1823'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='notification_email',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
