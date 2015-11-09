# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nouns', '__first__'),
        ('premises', '0025_auto_20151011_2241'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='premise',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='user',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.AddField(
            model_name='contention',
            name='nouns',
            field=models.ManyToManyField(related_name=b'contentions', to='nouns.Noun'),
            preserve_default=True,
        ),
    ]
