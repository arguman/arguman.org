# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('premises', '0035_premise_related_argument'),
    ]

    operations = [
        migrations.AlterField(
            model_name='premise',
            name='related_argument',
            field=models.ForeignKey(related_name=b'related_premises', blank=True, to='premises.Contention', help_text='You can also associate your premise with an argument.', null=True, verbose_name='Related Argument'),
        ),
    ]
