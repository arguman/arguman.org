# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('premises', '0022_auto_20141112_1823'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='report',
            unique_together=set([('reporter', 'premise', 'contention', 'fallacy_type')]),
        ),
    ]
