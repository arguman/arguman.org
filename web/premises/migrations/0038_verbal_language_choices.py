# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('premises', '0037_missing_migrations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contention',
            name='language',
            field=models.CharField(max_length=5, null=True, choices=[(b'tr', 'T\xfcrk\xe7e'), (b'en', 'English'), (b'ch', '\u4e2d\u6587'), (b'fr', 'Fran\xe7ais')]),
        ),
    ]
