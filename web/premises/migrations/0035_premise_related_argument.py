# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('premises', '0034_contention_is_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='premise',
            name='related_argument',
            field=models.ForeignKey(related_name=b'related_premises', blank=True, to='premises.Contention', help_text='You can link to an argument instead of your premise.', null=True),
            preserve_default=True,
        ),
    ]
