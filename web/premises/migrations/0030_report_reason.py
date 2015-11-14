# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('premises', '0029_contention_related_nouns'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='reason',
            field=models.TextField(help_text='Please explain that why the premise is a fallacy.', null=True, verbose_name='Reason'),
            preserve_default=True,
        ),
    ]
