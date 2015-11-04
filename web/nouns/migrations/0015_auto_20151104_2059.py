# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nouns', '0014_auto_20151104_0127'),
    ]

    operations = [
        migrations.AddField(
            model_name='noun',
            name='language',
            field=models.CharField(default='en', max_length=25),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='noun',
            name='text',
            field=models.CharField(max_length=255, db_index=True),
        ),
        migrations.AlterUniqueTogether(
            name='noun',
            unique_together=set([('text', 'language')]),
        ),
    ]
