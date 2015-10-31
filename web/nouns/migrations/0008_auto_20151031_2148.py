# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nouns', '0007_synonym_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noun',
            name='text',
            field=models.CharField(unique=True, max_length=255, db_index=True),
        ),
    ]
