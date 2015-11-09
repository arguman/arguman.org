# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nouns', '0013_remove_keyword_is_visible'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='noun',
            field=models.ForeignKey(related_name=b'keywords', to='nouns.Noun'),
        ),
        migrations.AlterField(
            model_name='relation',
            name='relation_type',
            field=models.CharField(max_length=25, choices=[(b'hypernym', 'is a'), (b'holonym', 'part of'), (b'antonym', 'opposite with')]),
        ),
    ]
