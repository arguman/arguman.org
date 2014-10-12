# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('premises', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='premise',
            name='parent',
            field=models.ForeignKey(related_name=b'children', blank=True, to='premises.Premise', null=True),
        ),
    ]
