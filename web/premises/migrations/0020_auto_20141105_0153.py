# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('premises', '0019_premise_date_creation'),
    ]

    operations = [
        migrations.AddField(
            model_name='contention',
            name='ip_address',
            field=models.IPAddressField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='premise',
            name='ip_address',
            field=models.IPAddressField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
