# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('premises', '0009_auto_20141023_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='premise',
            name='like_count',
            field=models.PositiveIntegerField(default=0, editable=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='premise',
            name='unlike_count',
            field=models.PositiveIntegerField(default=0, editable=False, db_index=True),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('premise', 'user')]),
        ),
    ]
