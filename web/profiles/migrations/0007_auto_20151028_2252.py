# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_profile_karma_point'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='karma_point',
            new_name='karma',
        ),
    ]
