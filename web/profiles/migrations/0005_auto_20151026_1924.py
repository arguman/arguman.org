# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_profile_notification_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='notification_email',
            field=models.BooleanField(default=True, verbose_name='email notification'),
        ),
    ]
