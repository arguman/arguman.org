# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '__first__'),
        ('premises', '0033_auto_20151115_2230'),
    ]

    operations = [
        migrations.AddField(
            model_name='contention',
            name='community',
            field=models.ForeignKey(blank=True, to='communities.Community', null=True),
            preserve_default=True,
        ),
    ]
